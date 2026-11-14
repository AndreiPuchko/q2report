import re
import pytest
from unittest.mock import patch, mock_open
from q2report import __version__
from q2report.q2report import Q2Report, Q2Report_rows
from q2report.q2printer.q2printer_docx import Q2PrinterDocx, points_in_cm as docx_points_in_cm
from q2report.q2printer.q2printer_xlsx import Q2PrinterXlsx, points_in_cm
from q2report.q2utils import is_sub_list, float_, num, set_dict_default

image_data = (
    "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABGdBT"
    "UEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAO"
    "pgAAA6mAAAF3CculE8AAAABmJLR0QAAAAAAAD5Q7t/AAAACXBIWXM"
    "AAABgAAAAYADwa0LPAAAAeElEQVRIx2NgGAUEACMRav5TYgYTrX3A"
    "QoFvCfmMPj4YtWBwWVDOAEkZ6JgQwKanHpdiXJb8J9JgvIZjs6SDC"
    "B80kGI4qZaQZTixllBkOCFLqGI4NsMasPCpArClLopdjs8Sog1nJs"
    "GCowyQIvsgAwNDI7VdP4IBAEbmQb9suzAuAAAAJXRFWHRkYXRlOmN"
    "yZWF0ZQAyMDIyLTA3LTE3VDA4OjQxOjA4KzAwOjAwJFqSuQAAACV0"
    "RVh0ZGF0ZTptb2RpZnkAMjAyMi0wNy0xN1QwODo0MTowOCswMDowM"
    "FUHKgUAAAAASUVORK5CYII="
)


demo_data = {
    "cursor": [
        {"data1": "XyDlguzuz", "num1": "5", "grp": 0, "tom": 1},
        {"data1": "XInjlysVB", "num1": "4", "grp": 0, "tom": 1},
        {"data1": "rUKcWIPkl", "num1": "6", "grp": 0, "tom": 2},
        {"data1": "fOBgKlaHr", "num1": "4", "grp": 0, "tom": 2},
        {"data1": "KBmHYMYQs", "num1": "9", "grp": 0, "tom": 3},
        {"data1": "FHuLGxKIe", "num1": "3", "grp": 0, "tom": 3},
        {"data1": "wGDrDFdmd", "num1": "3", "grp": 1, "tom": 1},
        {"data1": "jEHyRbKGx", "num1": "7", "grp": 1, "tom": 1},
        {"data1": "neLrvZQRP", "num1": "5", "grp": 1, "tom": 2},
        {"data1": "BXPKaXFSa", "num1": "9", "grp": 1, "tom": 2},
    ]
}


def test_version():
    assert __version__


def test_utils():
    assert is_sub_list([1, 2], [1, 2, 4])
    assert is_sub_list([1, 2], [1, 4, 8]) is False
    assert float_(0.15) == 0.15
    assert float_("0.15") == 0.15
    assert float_("error") == 0
    dic = {"key": 45}
    set_dict_default(dic, "key", 333)
    set_dict_default(dic, "key1", 333)
    assert dic["key"] == 45
    assert dic["key1"] == 333


def test_xlsx_image_is_centered_in_spanned_cell():
    printer = Q2PrinterXlsx("temp/test.xlsx")
    printer._cm_columns_widths = [2, 4]
    printer._columns_count = 2
    printer.current_sheet = {"drawing": [], "spans": [], "sheetData": []}

    style = {
        "text-align": "center",
        "vertical-align": "middle",
        "padding": "0",
        "font-size": "10pt",
        "font-family": "Calibri",
        "font-weight": "normal",
        "border-width": "0",
    }
    rows = {
        "heights": [0],
        "cells": {
            "0,0": {
                "colspan": 2,
                "rowspan": 1,
                "images": [
                    {
                        "image": image_data,
                        "width": 1,
                        "height": 1,
                        "pixel_width": 24,
                        "pixel_height": 24,
                    }
                ],
            }
        },
    }

    printer.render_rows_section(rows, style, 0)

    drawing = printer.current_sheet["drawing"][0]
    assert drawing["_col"] == 1
    assert drawing["_col_off_emu"] == int(num("0.5") * num(12700) * points_in_cm)


def test_docx_images_are_positioned_relative_to_their_cell():
    printer = Q2PrinterDocx("temp/test.docx")
    image = {
        "image": image_data,
        "width": 1,
        "height": 1,
        "pixel_width": 24,
        "pixel_height": 24,
    }
    styles_and_offsets = [
        ({"text-align": "left", "vertical-align": "top", "padding": "0.2"}, 0, 0),
        ({"text-align": "center", "vertical-align": "middle", "padding": "0.2"}, 0.3, 0.8),
        ({"text-align": "right", "vertical-align": "top", "padding": "0.2"}, 0.6, 0),
    ]

    for style, expected_left, expected_top in styles_and_offsets:
        image_xml = printer.get_cell_images(
            {"width": 2, "images": [image]}, style, cell_width=2, cell_height=3
        )

        assert 'layoutInCell="1"' in image_xml
        assert '<wp:positionH relativeFrom="character">' in image_xml
        assert '<wp:positionV relativeFrom="paragraph">' in image_xml
        cell_style = {**style, "border-width": "0", "font-size": "10pt", "font-family": "Calibri"}
        image_cell_xml = printer.add_table_cell(cell_style, "", 2, "", image_xml)
        assert "<w:vAlign" not in image_cell_xml
        actual_offsets = [int(offset) for offset in re.findall(r"<wp:posOffset>(\d+)</wp:posOffset>", image_xml)]
        expected_offsets = [
            int(num(expected_left) * num(12700) * docx_points_in_cm),
            int(num(expected_top) * num(12700) * docx_points_in_cm * num(0.94)),
        ]
        assert len(actual_offsets) == 2
        assert all(abs(actual - expected) <= 1 for actual, expected in zip(actual_offsets, expected_offsets))

    text_cell_xml = printer.add_table_cell(
        {"vertical-align": "middle", "text-align": "left", "border-width": "0", "padding": "0"}, "", 2, ""
    )
    assert '<w:vAlign w:val="center"/>' in text_cell_xml


def test_wrongs():
    report = Q2Report()
    with pytest.raises(Exception) as e:
        wrong_role = Q2Report_rows(role="123")


def test_load():
    report = Q2Report()
    with patch("builtins.open", mock_open(read_data="{}")) as filemock:
        with patch("os.path.isfile", return_value=True):
            report.load("123")
    report.load("{}")


def test_report():
    report = Q2Report()
    report.mydata.mydata = "123"

    report.add_page(page_margin_left=3)

    report.add_column(width=2)
    report.add_column()
    report.add_column(width="70%")

    report.add_rows(heights=[0, 0], style=report.make_style(font_size=20))
    report.add_row(height=0)

    report.set_cell(0, 0, "First <b>ce</b>ll", colspan=2, rowspan=2)
    report.set_cell(
        0,
        2,
        "{p1}",
        style=report.make_style(font_family="Courier", font_size=8, text_align="center", font_weight="bold"),
    )
    report.set_cell(1, 2, "{today()}", format="D")
    report.set_cell(2, 2, "**{float_(29/8)}**")
    report.set_cell(5, 2, "123456.25", format="F")
    report.set_cell(6, 2, "123456.25", format="N")
    report.set_cell(7, 2, "166cdsfs", format="D")

    report.set_cell(
        5,
        0,
        "Row six Col one",
        style=report.make_style(font_size=10, text_align="right", border_width="3 3 3 3", padding="0.5"),
    )

    report.set_cell(3, 2, "{q2image('%s',2)}" % image_data)
    report.set_cell(
        3,
        0,
        "{q2image('%(image_data)s')}{q2image('%(image_data)s',0,1)}{q2image('%(image_data)s')}" % globals(),
    )

    # Second page
    report.add_page(
        page_margin_left=2,
        page_margin_right=1,
        page_height=20,
        page_margin_bottom=2,
        page_width=20,
        page_margin_top=1,
        style=report.make_style(font_size=10),
    )

    report.add_columns(page_index=3, widths=[2, 2, 3, 0], style=report.make_style(border_width="1 0"))

    report.set_cell(
        0, 0, "Second page 1", style=report.make_style(font_size=10, vertical_align="center"), colspan=3
    )

    report.add_columns(widths=[2, 2, 5, 0])

    rows2_2 = report.add_rows(heights=[1, 2, 3, 4], style=report.make_style(font_size=8))
    rows2_2.set_cell(0, 0, "5555")

    report.set_cell(0, 0, "Second page 2 -row 1", style=report.make_style(font_size=10), colspan=4)
    report.set_cell(1, 3, "Second page 2 -row 2")

    report.set_cell(2, 0, "Second page 2 -rows 2")
    report.set_cell(3, 0, "{mydata}{no_data}")

    # table header and footer
    table_header = Q2Report_rows(style=report.make_style(text_align="center"))
    table_header.set_cell(0, 0, "Table", colspan=4, style=report.make_style(border_width="0", font_size=20))
    table_header.set_cell(1, 0, "Col 1")

    table_footer = Q2Report_rows()
    table_footer.set_cell(
        0, 0, "total", colspan=2, style=report.make_style(text_align="right", border_width="0")
    )
    table_footer.set_cell(0, 3, "{sum:num(num1)}", style=report.make_style(text_align="right"))

    # Group header and footer
    group_header = Q2Report_rows(style=report.make_style(text_align="center"))
    group_header.set_cell(0, 0, "Group headerr", colspan=4, style=report.make_style(border_width="2 0"))

    group_footer = Q2Report_rows()
    group_footer.set_cell(
        0, 0, "Group total", colspan=2, style=report.make_style(text_align="right", border_width="0")
    )
    group_footer.set_cell(0, 3, "{sum:num(num1)}", style=report.make_style(text_align="right", font_size=6))

    # Table
    table_row = Q2Report_rows(
        heights=[0, 0, 0],
        style=report.make_style(border_width="0", font_size=6),
        role="table",
        data_source="cursor",
    )
    table_row.set_cell(0, 0, "{data1}", style=report.make_style(text_align="center"))
    table_row.set_cell(
        0,
        1,
        "{rep.d.cursor.data1}{rep.d.cursor1.data1}{rep.d.cursor.data33}",
        style=report.make_style(text_align="center"),
    )
    table_row.set_cell(
        0,
        2,
        "{rep.d.cursor.r(2).data1} {rep.d.cursor.r(233).data1} {rep.d.cursor.getrow(5).data1}",
        style=report.make_style(text_align="center"),
    )
    table_row.set_cell(0, 3, "{num1}", style=report.make_style(text_align="right"))
    table_row.set_table_header(table_header)
    table_row.set_table_footer(table_footer)
    table_row.add_table_group("grp", group_header, group_footer)

    report.add_rows(rows=table_row)

    report.add_columns(widths=[])
    report.add_columns(widths=[1])

    row1 = Q2Report_rows(role="table", data_source="wrong_ds")
    row1.set_cell(0, 1, "123")
    report.add_rows(rows=row1)

    report.add_page(page_height=10)
    report.set_cell(0, 0, "small page")

    report.params["p1"] = " <b>bold text</b> just text"

    with patch("builtins.open", mock_open()) as filemock:
        report.run("temp/repo.docx", data=demo_data, open_output_file=False)
        report.run("temp/repo.xlsx", data=demo_data, open_output_file=False)
        report.run("temp/repo.html", data=demo_data, open_output_file=False)

    with pytest.raises(BaseException) as e:
        report.run("temp/repo.rtf", data=demo_data, open_output_file=False)


if __name__ == "__main__":  # pragma: no cover
    test_report()
