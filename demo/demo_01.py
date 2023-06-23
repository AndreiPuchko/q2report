from q2report.q2report import Q2Report, report_rows

import random
import string
import os
import json


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
    # Second page
    report.add_page(page_margin_left=2)

    report.add_columns(widths=[2, 2, 3, 0])

    report.set_cell(4, 0, "Second page 1", style=report.make_style(font_size=10), colspan=3)

    report.add_columns(widths=[2, 2, 5, 0])

    rows2_2 = report.add_rows(heights=[1, 2, 3, 4], style=report.make_style(font_size=8))
    rows2_2.set_cell(10, 0, "5555")

    report.set_cell(0, 0, "Second page 2 -row 1", style=report.make_style(font_size=10), colspan=4)
    report.set_cell(1, 3, "Second page 2 -row 2")

    report.set_cell(3, 0, "Second page 2 -rows 2")

    table_row = report_rows(heights=[0, 0, 0], style=report.make_style(border_width="0", font_size=6))
    table_row.set_cell(1, 1, "55555")
    report.add_rows(rows=table_row)

    report.params["p1"] = " <b>bold text</b> just text"
    # print(json.dumps(report.report_content, indent=2))

    # res_file = report.run("temp/repo.html", data=demo_data, open_output_file=False)
    # res_file = report.run("temp/repo.xlsx", data=demo_data, open_output_file=False)
    res_file = report.run("temp/repo.docx", data=demo_data, open_output_file=False)

    os.system(os.path.abspath(res_file))


if __name__ == "__main__":
    demo()
