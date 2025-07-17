from q2report.q2report import Q2Report, Q2Report_rows

import os


def demo_udf():
    return "demo udf"


def demo():
    demo_data = {"cursor": []}

    # for x in range(100):
    #     demo_data["cursor"].append(
    #         {
    #             "data1": "".join([random.choice(string.ascii_letters) for x in range(9)]),
    #             "num1": f"{random.randint(3,10)}",
    #             "grp": int(x / random.randint(6, 10)),
    #             "tom": int(random.randint(1, 2)),
    #         }
    #     )

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

    report = Q2Report()
    report.mydata.mydata = "123"
    c13 = 25
    report.set_data(demo_udf)
    # report.set_data(c13, "13")

    # report.data["mydata"] = "123"
    # Firt page
    if 1:
        report.add_page(page_margin_left=3)

        report.add_column(width=2)
        # report.add_column()
        # report.add_column(width="10")

        report.add_rows(heights=[0], style=report.make_style(font_size=16))
        # report.add_row(height=0)
        # report.set_cell(0, 0, "{demo_udf()}")
        # report.set_cell(0, 1, "{mydata}")
        # report.set_cell(0, 2, "{13}")

        report.set_cell(0, 0, "{q2image('%s',4)}" % image_data, style=report.make_style(padding="0"))
        report.set_cell(0, 1, "{13}")

        if 0:
            report.set_cell(0, 0, "First <b>ce</b>ll", colspan=2, rowspan=2)
            report.set_cell(2, 0, "**{mydata}")
            report.set_cell(
                0,
                2,
                "{p1}",
                style=report.make_style(
                    font_family="Courier", font_size=8, text_align="center", font_weight="bold"
                ),
            )
            report.set_cell(1, 2, "{today()}", format="D")
            report.set_cell(2, 2, "**{float_(29/8)}**")
            report.set_cell(5, 2, "123456.78", format="F")
            report.set_cell(
                5,
                0,
                "Row six Col one",
                # style=report.make_style(font_size=10, text_align="right", border_width="3 3 3 3", padding="0.5"),
                style="{border-width: 3 3 3 3; padding:1}",
            )

            report.set_cell(
                3,
                0,
                "{q2image('%(image_data)s')}{q2image('%(image_data)s',0,1)}{q2image('%(image_data)s',3,3)}"
                % locals(),
            )

    if 0:
        # Second page
        report.add_page(
            page_margin_left=2,
            page_margin_right=1,
            page_width=20,
            page_height=22,
            page_margin_bottom=2,
            page_margin_top=1,
            style=report.make_style(font_size=10),
        )
        if 1:
            report.add_columns(widths=[2, 2, 3, 0])

            report.set_cell(0, 0, "Second page 1", style=report.make_style(font_size=10), colspan=3)

            report.add_columns(widths=[2, 2, 5, 0])

            rows2_2 = report.add_rows(heights=[1, 2, 3, 4], style=report.make_style(font_size=8))
            rows2_2.set_cell(0, 0, "5555")

            report.set_cell(0, 0, "Second page 2 -row 1", style=report.make_style(font_size=10), colspan=4)
            report.set_cell(1, 3, "Second page 2 -row 2")

            report.set_cell(2, 0, "Second page 2 -rows 2")
        # table header and footer
        table_header = Q2Report_rows(style=report.make_style(text_align="center"))
        table_header.set_cell(0, 0, "Table", colspan=4, style=report.make_style(border_width="0", font_size=20))
        table_header.set_cell(1, 0, "Col 1")

        table_footer = Q2Report_rows()
        table_footer.set_cell(
            0,
            0,
            "Total",
            colspan=2,
            style=report.make_style(text_align="right", border_width="0", font_weight="bold"),
        )
        table_footer.set_cell(0, 3, "{sum:num(num1)}", style=report.make_style(text_align="right"))

        # Group header and footer
        group_header = Q2Report_rows(style=report.make_style(text_align="center"))
        group_header.set_cell(
            0, 0, "Group header {_group_number}!", colspan=4, style=report.make_style(border_width="2 0")
        )

        group_footer = Q2Report_rows()
        group_footer.set_cell(
            0,
            0,
            "Group total ({_group_number})",
            colspan=2,
            style=report.make_style(text_align="right", border_width="0"),
        )
        group_footer.set_cell(0, 3, "{sum:num(num1)}", style=report.make_style(text_align="right", font_size=6))

        # Table
        table_row = Q2Report_rows(
            heights=[0, 0, 0],
            style=report.make_style(border_width="0", font_size=6),
            role="table",
            data_source="cursor",
        )
        table_row.set_cell(
            0,
            0,
            "{_row_number}-{_grow_number}-{data1} - {_group_number}",
            style=report.make_style(text_align="center"),
        )
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

        report.add_page(page_height=10, page_width=10)
        report.set_cell(0, 0, "small page0")
        this_rows = report.set_cell(2, 2, "small page2")
        this_rows.set_row_height(2, "4-0")
        report.set_col_width(column=1, width="1")
        report.set_col_width(column=2, width="50%")

    report.params["p1"] = " <b>bold text</b> just text"
    # print(json.dumps(report.report_content, indent=2))

    # res_file = report.run("temp/repo.html", data=demo_data, open_output_file=False)
    res_file = report.run("temp/repo.xlsx", data=demo_data, open_output_file=False)
    # res_file = report.run("temp/repo.docx", data=demo_data, open_output_file=False)

    os.system(os.path.abspath(res_file))


if __name__ == "__main__":  # pragma: no cover
    demo()
