from q2report.q2report import Q2Report, Q2Report_rows

import os


def demo_udf():
    return "demo udf"


def demo(type="pdf", open_output_file=True):
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

    report = Q2Report()
    cell_image = "{'%s':I3*3}123" % image_data
    report.add_rows(heights=[2, 12], style=report.make_style(font_size=16))
    report.set_cell(0, 0, cell_image, style=report.make_style(padding=0, alignment=7))
    # report.set_cell(0, 1, cell_image, style=report.make_style(padding=0, alignment=9), colspan=2)
    report.set_cell(0, 1, "text", colspan=2, style=report.make_style(alignment=6))
    report.set_cell(
        1,
        0,
        "{'%s':I3*3}456" % image_data,
        style=report.make_style(padding=0, alignment=5),
        colspan=2,
        rowspan=2,
    )

    report.run(f"temp/repo.{type}", open_output_file=open_output_file)


if __name__ == "__main__":  # pragma: no cover
    demo()
