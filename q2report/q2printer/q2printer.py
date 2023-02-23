if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")
    from demo.demo_00 import demo

    demo()

import os
from q2report.q2utils import num
import sys
import subprocess


def get_printer(output_file, output_type=None):
    if output_type is None and isinstance(output_file, str):
        output_type = os.path.splitext(output_file)[1].lower().replace(".", "")

    if output_type == "html":
        from q2report.q2printer.q2printer_html import Q2PrinterHtml as _printer
    elif output_type == "xlsx":
        from q2report.q2printer.q2printer_xlsx import Q2PrinterXlsx as _printer
    elif output_type == "docx":
        from q2report.q2printer.q2printer_docx import Q2PrinterDocx as _printer
    else:
        raise BaseException(f"format {output_type} is not supported")
    return _printer(output_file, output_type)


class Q2Printer:
    def __init__(self, output_file, output_type=None):
        self.output_file = output_file
        if output_type is None and isinstance(self.output_file, str):
            output_type = os.path.splitext(output_file)[1]
        self.output_type = output_type.lower().replace(".", "")
        self.xmlImageList = []
        self._OF = None
        self._columns_count = None
        self._cm_columns_widths = []
        self.q2report = None
        self.open_output_file()

    def open_output_file(self):
        # if not os.path.isdir(os.path.dirname(self.output_file)):
        #     os.mkdir(os.path.dirname(self.output_file))
        self._OF = open(self.output_file, "w", encoding="utf8")

    def calculate_real_sizes(self, rows_section, style):
        row_count = len(rows_section["heights"])
        spanned_key = []
        rows_section["real_heights"] = [0 for x in range(row_count)]
        rows_section["max_cell_height"] = [0 for x in range(row_count)]
        for row in range(row_count):
            for col in range(self._columns_count):
                key = f"{row},{col}"
                cell_data = rows_section.get("cells", {}).get(key, {})
                if cell_data.get("rowspan", 0) > 1 or cell_data.get("colspan", 0) > 1:
                    spanned_key.append(key)

                if not cell_data:
                    continue
                if cell_data.get("colspan", 0) > 1:
                    cell_data["width"] = sum(self._cm_columns_widths[col : col + cell_data["colspan"]])
                else:
                    cell_data["width"] = self._cm_columns_widths[col]
                if cell_data.get("data"):
                    cell_data["height"] = self.q2report.get_cell_height(cell_data)
                    if rows_section["max_cell_height"][row] < cell_data["height"]:
                        rows_section["max_cell_height"][row] = cell_data["height"]
                # TODO: if background image (how to know?) - do not change height
                for image in cell_data.get("images", []):
                    w, h, i = self.prepare_image(image, cell_data.get("width"))
                    rows_section["real_heights"][row] = (
                        rows_section["real_heights"][row] if rows_section["real_heights"][row] >= h else h
                    )
                    if rows_section["max_cell_height"][row] < rows_section["real_heights"][row]:
                        rows_section["max_cell_height"][row] = rows_section["real_heights"][row]
        print(spanned_key)

    def render_rows_section(self, rows, style, outline_level):
        self.calculate_real_sizes(rows, style)

    def reset_page(
        self,
        page_width=21.0,
        page_height=29.0,
        page_margin_left=2.0,
        page_margin_top=1.0,
        page_margin_right=1.0,
        page_margin_bottom=1.0,
        last_page=False,
    ):
        self.page_width = num(page_width)
        self.page_height = num(page_height)
        self.page_margin_left = num(page_margin_left)
        self.page_margin_right = num(page_margin_right)
        self.page_margin_top = num(page_margin_top)
        self.page_margin_bottom = num(page_margin_bottom)
        self._current_width = self.page_width - self.page_margin_left - self.page_margin_right
        self._current_height = self.page_height - self.page_margin_top - self.page_margin_bottom

    def reset_columns(self, widths=[]):
        self._columns_count = len(widths)
        _cm_page_width = self._current_width

        self._cm_columns_widths = [0 for x in range(self._columns_count)]

        _fixed_columns_width = [num(x) if "%" not in x and num(x) != 0 else 0 for x in widths]
        _procent_columns_width = [num(x.replace("%", "").strip()) if "%" in x else 0 for x in widths]
        _float_columns_count = (
            self._columns_count
            - len([x for x in _procent_columns_width if x != 0])
            - len([x for x in _fixed_columns_width if x != 0])
        )
        _procent_width = num((_cm_page_width - num(sum(_fixed_columns_width))) / num(100))

        for x in range(self._columns_count):
            if _fixed_columns_width[x] != 0:
                self._cm_columns_widths[x] = _fixed_columns_width[x]
            else:
                prc = _procent_columns_width[x]
                if prc == 0:
                    prc = (num(100) - sum(_procent_columns_width)) / _float_columns_count
                self._cm_columns_widths[x] = round(_procent_width * prc, 2)
        self._cm_columns_widths = [round(x, 2) for x in self._cm_columns_widths]

    def prepare_image(self, image_dict, col_width):
        # col_width = self._cm_columns_widths[col]
        image = image_dict["image"]
        width = image_dict["width"]
        height = image_dict["height"]
        pixel_width = image_dict["pixel_width"]
        pixel_height = image_dict["pixel_height"]

        if image not in self.xmlImageList:
            self.xmlImageList.append(image)
            imageIndex = len(self.xmlImageList) - 1
        else:
            imageIndex = self.xmlImageList.index(image)

        if height == 0:
            if width == 0:
                width = num(col_width)
            height = width * pixel_height / pixel_width
        elif width == 0 and height != 0:
            width = height * pixel_width / pixel_height

        return width, height, imageIndex

    def save(self):
        self._OF.close()

    def show(self):
        if os.path.isfile(self.output_file):
            if sys.platform[:3] == "win":
                os.startfile(os.path.abspath(self.output_file))
                # subprocess.Popen(
                #     ["start", os.path.abspath(self.output_file)],
                #     close_fds=True, 
                #     shell=True,
                #     creationflags=subprocess.DETACHED_PROCESS,
                # )
            # elif sys.platform == 'darwin':
            #     subprocess.Popen(["open", self.output_file], close_fds=True, shell=False)
            else:
                subprocess.Popen(["open", self.output_file], close_fds=True, shell=False)
