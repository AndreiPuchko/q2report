import os
import sys
import re
import glob
from q2report.q2utils import num, int_, reMultiSpaceDelete
from q2report.q2printer.q2printer import Q2Printer, pyqt6_installed

# Константы для расчетов
points_in_cm = num(28.34645669)  # 1cm = 28.34645669 pt
inch_in_cm = num(2.54)  # 1 дюйм = 2.54 см
CM_TO_INCH = 0.3937007874


# Для удобства, чтобы не зависеть от внешней getCSSvalue
def getCSSvalue(style_dict, key, default=""):
    """Извлекает значение из словаря стилей q2report."""
    if isinstance(style_dict, str):
        # Если случайно передали строку, возвращаем пустую строку
        return default
    return style_dict.get(key, default)


reSpaces = re.compile(r"\s+")

if pyqt6_installed:
    from PyQt6.QtGui import (
        QTextDocument,
        QPageLayout,
        QPageSize,
        QFont,
        QColor,
        QImage,
        QPainter,
        QPen,
        QTextOption,
        QTextBlockFormat,
        QFontMetricsF,
    )
    from PyQt6.QtCore import QSizeF, Qt, QByteArray, QIODevice, QMarginsF, QRectF, QPointF, QSize, QRect
    from PyQt6.QtPrintSupport import QPrinter


class Q2PrinterPdf(Q2Printer):
    def __init__(self, output_file, output_type=None):
        super().__init__(output_file, output_type)
        if not pyqt6_installed:
            raise ImportError("PyQt6 is required for Q2PrinterPdf")

        self.printer = QPrinter()
        self.printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        self.printer_resolution = 300
        self.printer.setResolution(self.printer_resolution)
        self.cm_to_points = self.printer_resolution / 2.54

        self.printer.setOutputFileName(self.output_file)
        self.printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        self.printer.setFullPage(True)

        self.textDoc = QTextDocument()
        self.base_font = QFont("Calibri", 10)
        self.textDoc.setDefaultFont(self.base_font)
        self.textDoc.setDocumentMargin(0)
        
        self.defaultTextOption = QTextOption()
        self.defaultTextOption.setWrapMode(QTextOption.WrapMode.WrapAtWordBoundaryOrAnywhere)

        self.page_layout = QPageLayout()
        self.painter = QPainter()
        self.painter.begin(self.printer)
        self.painter.scale(self.cm_to_points, self.cm_to_points)
        self.pen_width = 2 / 96 / 2.54
        self.painter.setPen(QPen(self.painter.brush(), self.pen_width))

        self.current_y_cm = 0.0  # Текущая позиция Y в CM

        self.currentVAlign = Qt.AlignmentFlag.AlignTop  # Вертикальное выравнивание

        if not hasattr(self, "format"):
            self.format = ""

        # Настройки по умолчанию
        self.reset_page()

    def _cm_to_points(self, cm):
        """Конвертирует сантиметры в точки (pt)."""
        return num(cm) * points_in_cm

    def reset_page(self, **args):
        super().reset_page(**args)

        if self.painter.isActive():
            self.painter.end()

        # 1. Настройка QPrinter (CM -> MM)
        page_size_mm = QSizeF(float(self.page_width * 10), float(self.page_height * 10))
        page_size = QPageSize(page_size_mm, QPageSize.Unit.Millimeter, "CustomPageSize")

        if self.page_width > self.page_height:
            orientation = QPageLayout.Orientation.Landscape
        else:
            orientation = QPageLayout.Orientation.Portrait

        self.page_layout.setPageSize(page_size)
        self.page_layout.setOrientation(orientation)

        # Отступы в точках (pt)
        margin_left_pt = self._cm_to_points(self.page_margin_left)
        margin_top_pt = self._cm_to_points(self.page_margin_top)
        margin_right_pt = self._cm_to_points(self.page_margin_right)
        margin_bottom_pt = self._cm_to_points(self.page_margin_bottom)
        # self.page_layout.setMargins(
        #     QMarginsF(margin_left_pt, margin_top_pt, margin_right_pt, margin_bottom_pt)
        # )

        self.printer.setPageLayout(self.page_layout)
        self.printer.setPageOrientation(orientation)
        self.current_y_cm = self.page_margin_top
        self.painter.begin(self.printer)
        self.painter.scale(self.cm_to_points, self.cm_to_points)

    def newPage(self, height_needed):
        """Проверяет, поместится ли элемент, и начинает новую страницу, если нужно."""
        page_end_cm = self.page_height - self.page_margin_bottom

        if self.current_y_cm + height_needed > page_end_cm:
            self.painter.end()
            self.printer.newPage()
            self.current_y_cm = self.page_margin_top
            self.painter.begin(self.printer)
            self.painter.scale(self.cm_to_points, self.cm_to_points)

    def save(self):
        super().save()
        if self.painter and self.painter.isActive():
            self.painter.end()

    def setFormats(self, style):
        """Устанавливает форматы шрифта, блока и сохраняет вертикальное выравнивание."""

        # 1. Настройка Шрифта (QCharFormat)
        font = QFont(style.get("font-family", self.base_font))

        if font_size := style.get("font-size", "10pt"):
            pt_size = num(font_size.lower().replace("pt", ""))
            font.setPixelSize(int(int(pt_size) * self.printer_resolution / 72))

        if font_weight := style.get("font-weight", ""):
            font.setBold(font_weight == "bold" or num(font_weight) >= 700)

        if font_style := style.get("font-style", ""):
            font.setItalic(font_style == "italic")

        if font_style := style.get("text-decoration", ""):
            font.setUnderline(font_style == "underline")

        css_style = []
        css_style.append(f"color: {style.get('color', 'black')}")

        self.textDoc.setDefaultFont(font)
        self.textDoc.setDefaultStyleSheet("p { %s }" % ";".join(css_style))

        if align := style.get("text-align", "left"):
            if align == "center":
                self.defaultTextOption.setAlignment(Qt.AlignmentFlag.AlignCenter)
            elif align == "right":
                self.defaultTextOption.setAlignment(Qt.AlignmentFlag.AlignRight)
            elif align == "justify":
                self.defaultTextOption.setAlignment(Qt.AlignmentFlag.AlignJustify)
            else:
                self.defaultTextOption.setAlignment(Qt.AlignmentFlag.AlignLeft)
        else:
            self.defaultTextOption.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.textDoc.setDefaultTextOption(self.defaultTextOption)

        # 3. Сохраняем Вертикальное выравнивание для putBox
        if valign := style.get("vertical-align", "top"):
            if valign == "bottom":
                self.currentVAlign = Qt.AlignmentFlag.AlignBottom
            elif valign == "middle":
                self.currentVAlign = Qt.AlignmentFlag.AlignVCenter
            else:
                self.currentVAlign = Qt.AlignmentFlag.AlignTop
        else:
            self.currentVAlign = Qt.AlignmentFlag.AlignTop

    def setMargins(self, style):
        """Устанавливает отступы в textDoc (для расчета высоты) и возвращает CM-значения."""
        padding_cm_str = style.get("padding", "0.05cm 0.05cm 0.05cm 0.05cm")
        padding_cm_list = reSpaces.split(padding_cm_str.lower().replace("cm", ""))
        padding_cm = [num(v) for v in padding_cm_list]

        # Нормализация до 4 значений (Top, Right, Bottom, Left)
        if len(padding_cm) == 1:
            padding_cm = [padding_cm[0]] * 4
        elif len(padding_cm) == 2:
            padding_cm = [padding_cm[0], padding_cm[1], padding_cm[0], padding_cm[1]]
        elif len(padding_cm) == 3:
            padding_cm = [padding_cm[0], padding_cm[1], padding_cm[2], padding_cm[1]]
        elif len(padding_cm) != 4:
            padding_cm = ["0.05cm"] * 4

        return padding_cm[0], padding_cm[1], padding_cm[2], padding_cm[3]

    def draw_cell(self, cell_data, left_cm=0, top_cm=0, width_cm=5, height_cm=5, style=""):
        txt = cell_data.get("data", "")
        rect_cm = QRectF(left_cm, top_cm, width_cm, height_cm)
        self.draw_cell_borders(rect_cm, style)

        """Отрисовывает содержимое ячейки и ее рамки."""
        # Используем переданный 'format', так как он уже содержит полный, объединенный стиль
        if txt != "":  # есть что выводить
            self.setFormats(style)
            p_top, p_right, p_bottom, p_left = self.setMargins(style)

            rect = QRectF(
                (left_cm + p_left), top_cm + p_top, width_cm - p_left - p_right, height_cm - p_top - p_bottom
            )
            
            # Установка ширины документа (в пикселях)
            self.textDoc.setTextWidth(rect.width() * self.cm_to_points)
            self.textDoc.setHtml(f"<p>{txt}</p>")

            
            
            # font = QFont("Times New Roman")
            # font.setPixelSize(int(14 * self.printer_resolution / 72))
            # self.textDoc.setDefaultFont(font)

            top_offset_cm = 0
            cell_height_cm = rect.height()

            docHeight_cm = self.textDoc.size().height() / self.cm_to_points

            if docHeight_cm < height_cm:
                if self.currentVAlign == Qt.AlignmentFlag.AlignVCenter:
                    top_offset_cm += (cell_height_cm - docHeight_cm) / 2
                elif self.currentVAlign == Qt.AlignmentFlag.AlignBottom:
                    top_offset_cm += cell_height_cm - docHeight_cm

            print(cell_data["height"], height_cm, txt, docHeight_cm, top_offset_cm)

            self.painter.save()
            self.painter.resetTransform()
            self.painter.translate(rect.left() * self.cm_to_points, rect.top() * self.cm_to_points + top_offset_cm * self.cm_to_points )
            textRect = QRectF(0, 0, rect.width() * self.cm_to_points, rect.height() * self.cm_to_points)
            # self.painter.drawRect(textRect)
            self.textDoc.drawContents(self.painter, textRect)
            self.painter.restore()

    def draw_cell_borders(self, rect_cm, style):
        self.painter.fillRect(rect_cm, QColor(style.get("background", "white")))

        b_width_str = style.get("border-width", "0cm").lower().replace("cm", "")
        b_width_cm = reSpaces.split(b_width_str)
        b_color = style.get("border-color", "black")

        # Нормализация до 4 значений (top, right, bottom, left)
        b = [float(num(v)) for v in b_width_cm]
        while len(b) < 4:
            b.append(b[0])

        color = QColor(b_color)
        lastPen = self.painter.pen()

        leftPoint = rect_cm.left()
        topPoint = rect_cm.top()
        w = rect_cm.width()
        h = rect_cm.height()

        if b[0] > 0:  # top
            self.painter.setPen(QPen(color, b[0] * self.pen_width))
            self.painter.drawLine(QPointF(leftPoint, topPoint), QPointF(leftPoint + w, topPoint))

        if b[1] > 0:  # right
            self.painter.setPen(QPen(color, b[1] * self.pen_width))
            self.painter.drawLine(QPointF(leftPoint + w, topPoint), QPointF(leftPoint + w, topPoint + h))

        if b[2] > 0:  # bottom
            self.painter.setPen(QPen(color, b[2] * self.pen_width))
            self.painter.drawLine(QPointF(leftPoint, topPoint + h), QPointF(leftPoint + w, topPoint + h))

        if b[3] > 0:  # left
            self.painter.setPen(QPen(color, b[3] * self.pen_width))
            self.painter.drawLine(QPointF(leftPoint, topPoint), QPointF(leftPoint, topPoint + h))
        self.painter.setPen(lastPen)

    def render_rows_section(self, rows_section, style, outline_level):
        super().render_rows_section(rows_section, style, outline_level)
        spanned_cells_to_skip = {}
        # print(rows_section["heights"])
        # print(self._cm_columns_widths)
        for row in range(len(rows_section["heights"])):
            current_x_cm = self.page_margin_left
            row_height_cm = rows_section["row_height"][row]
            self.newPage(row_height_cm)
            for col in range(self._columns_count):
                key = f"{row},{col}"
                if key in spanned_cells_to_skip:
                    current_x_cm += self._cm_columns_widths[col]
                    continue

                cell_data = rows_section.get("cells", {}).get(key, {})
                cell_width_cm = self._cm_columns_widths[col]

                row_span = int_(cell_data.get("rowspan", 1))
                col_span = int_(cell_data.get("colspan", 1))
                cell_style = cell_data.get("style", {})

                final_style = dict(style)
                final_style.update(cell_style)

                if col_span > 1:
                    cell_width_cm = sum(self._cm_columns_widths[col : col + col_span])

                if row_span > 1:
                    actual_row_height_cm = sum(rows_section["row_height"][row + i] for i in range(row_span))
                else:
                    actual_row_height_cm = row_height_cm

                if row_span > 1 or col_span > 1:
                    for tmp_span_row in range(row_span):
                        for tmp_span_col in range(col_span):
                            span_key = f"{tmp_span_row+row},{tmp_span_col+col}"
                            if (tmp_span_row > 0 or tmp_span_col > 0) and span_key != key:
                                spanned_cells_to_skip[span_key] = True

                self.draw_cell(
                    cell_data,
                    current_x_cm,
                    self.current_y_cm,
                    cell_width_cm,
                    actual_row_height_cm,
                    final_style,
                )
                # return
                current_x_cm += self._cm_columns_widths[col]

            self.current_y_cm += row_height_cm
