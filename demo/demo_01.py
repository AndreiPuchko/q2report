from q2report.q2report import Q2Report, report_rows, re_q2image

import random
import string
import os
import json
import codecs


def demo():
    demo_data = {"cursor": []}

    for x in range(100):
        demo_data["cursor"].append(
            {
                "data1": "".join([random.choice(string.ascii_letters) for x in range(9)]),
                "num1": f"{random.randint(3,10)}",
                "grp": int(x / random.randint(6, 10)),
                "tom": int(random.randint(1, 2)),
            }
        )

    image_data = """89504E470D0A1A0A0000000D4948445200000018000000180806000000E
                    0773DF80000000467414D410000B18F0BFC6105000000206348524D0000
                    7A26000080840000FA00000080E8000075300000EA6000003A980000177
                    09CBA513C00000006624B4744000000000000F943BB7F00000009704859
                    73000000600000006000F06B42CF000000784944415448C763601805040
                    023116AFE53620613AD7DC042816F09F98C3E3E18B560705950CE004919
                    E89810C0A6A71E97625C96FC27D260BC8663B3A483081F34906238A9969
                    06538B196506438214BA8623836C31AB0F0A902B0A52E8A5D8ECF12A20D
                    6726C182A30C9022FB2003034323B55D3F82010046E641BF6CBB302E000
                    0002574455874646174653A63726561746500323032322D30372D313754
                    30383A34313A30382B30303A3030245A92B900000025744558746461746
                    53A6D6F6469667900323032322D30372D31375430383A34313A30382B30
                    303A303055072A050000000049454E44AE426082"""
    image_data = image_data.replace("\n", "").replace(" ", "")
    image_data = codecs.encode(codecs.decode(image_data, "hex"), "base64").decode().replace("\n", "")
    print(image_data)

    # image_data = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QAAAAAAAD5Q7t/AAAACXBIWXMAAABgAAAAYADwa0LPAAAAeElEQVRIx2NgGAUEACMRav5TYgYTrX3AQoFvCfmMPj4YtWBwWVDOAEkZ6JgQwKanHpdiXJb8J9JgvIZjs6SDCB80kGI4qZaQZTixllBkOCFLqGI4NsMasPCpArClLopdjs8Sog1nJsGCowyQIvsgAwNDI7VdP4IBAEbmQb9suzAuAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDIyLTA3LTE3VDA4OjQxOjA4KzAwOjAwJFqSuQAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyMi0wNy0xN1QwODo0MTowOCswMDowMFUHKgUAAAAASUVORK5CYII="

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

    report = Q2Report()
    # Firt page
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
    report.set_cell(
        5,
        0,
        "Row six Col one",
        style=report.make_style(font_size=10, text_align="right", border_width="3 3 3 3", padding="0.5"),
    )

    report.set_cell(4, 2, "{q2image('%s',3,4)}" % image_data)

    # Second page
    report.add_page(page_margin_left=2)

    report.add_columns(widths=[2, 2, 3, 0])

    report.set_cell(0, 0, "Second page 1", style=report.make_style(font_size=10), colspan=3)

    report.add_columns(widths=[2, 2, 5, 0])

    rows2_2 = report.add_rows(heights=[1, 2, 3, 4], style=report.make_style(font_size=8))
    rows2_2.set_cell(0, 0, "5555")

    report.set_cell(0, 0, "Second page 2 -row 1", style=report.make_style(font_size=10), colspan=4)
    report.set_cell(1, 3, "Second page 2 -row 2")

    report.set_cell(2, 0, "Second page 2 -rows 2")
    # table header and footer
    table_header = report_rows(style=report.make_style(text_align="center"))
    table_header.set_cell(0, 0, "Table", colspan=4, style=report.make_style(border_width="0", font_size=20))
    table_header.set_cell(1, 0, "Col 1")

    table_footer = report_rows()
    table_footer.set_cell(
        0, 0, "total", colspan=2, style=report.make_style(text_align="right", border_width="0")
    )
    table_footer.set_cell(0, 3, "{sum:num(num1)}", style=report.make_style(text_align="right"))

    # Group header and footer
    group_header = report_rows(style=report.make_style(text_align="center"))
    group_header.set_cell(0, 0, "Group headerr", colspan=4, style=report.make_style(border_width="2 0"))

    group_footer = report_rows()
    group_footer.set_cell(
        0, 0, "Group total", colspan=2, style=report.make_style(text_align="right", border_width="0")
    )
    group_footer.set_cell(0, 3, "{sum:num(num1)}", style=report.make_style(text_align="right", font_size=6))

    # Table
    table_row = report_rows(
        heights=[0, 0, 0],
        style=report.make_style(border_width="0", font_size=6),
        role="table",
        data_source="cursor",
    )
    table_row.set_cell(0, 0, "{data1}", style=report.make_style(text_align="center"))
    table_row.set_cell(0, 3, "{num1}", style=report.make_style(text_align="right"))
    table_row.set_table_header(table_header)
    table_row.set_table_footer(table_footer)
    table_row.add_table_group("grp", group_header, group_footer)

    report.add_rows(rows=table_row)

    report.params["p1"] = " <b>bold text</b> just text"
    # print(json.dumps(report.report_content, indent=2))

    # res_file = report.run("temp/repo.html", data=demo_data, open_output_file=False)
    # res_file = report.run("temp/repo.xlsx", data=demo_data, open_output_file=False)
    res_file = report.run("temp/repo.docx", data=demo_data, open_output_file=False)

    os.system(os.path.abspath(res_file))


if __name__ == "__main__":
    demo()
