from q2report.q2report import Q2Report
import os


def demo(type="pdf"):
    report = Q2Report()
    report.set_style(report.make_style(border_width="1"))
    report.add_page(page_margin_left=2, page_height=21, page_width=21)
    # report.add_rows(heights=["1-0", "0-2"])

    report.add_column(width="20%")
    report.add_column(width=0)
    report.add_column(width="8%")

    report.set_cell(
        0,
        0,
        data=" Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed "
        " do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        " Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris "
        "nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in ",
        rowspan=1,
        style={
            "background": "black",
            "color": "white",
            "font-style": "italic",
            "text-decoration": "underline",
        },
    )
    report.set_cell(0, 1, data="123", style={"font-weight": "bold", "font-size": 50, "border-width": "20 1 2 12", "border-color": "green"})
    report.set_cell(0, 2, data=" Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed ", rowspan=2)
    report.set_cell(
        1,
        1,
        data="1 <i>Lorem</i> ipsum dolor sit <u>amet</u>, consectetur adipiscing elit, sed "
        " do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        " Ut<br> enim ad <font size=+1 color=#0000FF>minim</font> veniam, quis nostrud exercitation ullamco "
        "laboris nisi ut aliquip ex ea <b>commodo consequat</b>. Duis aute irure dolor in "
        "reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla "
        "pariatur. Excepteur sint occaecat cupidatat non proident, sunt in "
        "culpa qui officia deserunt mollit anim id est laborum. "
        "",
        rowspan=2,
    )

    report.set_cell(
        7,
        0,
        data=" Lorem ipsum <font size=+2>sdg <b>sd</b>iog</font> isdg sdg ;sdf gskfdn gklsjdn",
    )

    print(report.report_content)
    # report.set_data(b, "a")

    res_file = report.run(f"temp/repo.{type}", open_output_file=False)
    os.system(os.path.abspath(res_file))


if __name__ == "__main__":  # pragma: no cover
    demo()
