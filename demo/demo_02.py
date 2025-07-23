from q2report.q2report import Q2Report, Q2Report_rows
import os


def demo():
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
        "supplier": [{"name": "Things and services", "address": "Park Lane, 5", "id": 1}],
        "customer": [{"name": "Buy and sell company", "address": "Big Rock street, 568", "id": 45}],
        "invoice": [
            {
                "number": "46521/169-00",
                "date": "2023-12-12",
                "comments": "Emergency deal",
                "expire_date": "2023-12-22",
                "discount": "5.5",
            }
        ],
        "items": [
            {"id": "45", "name": "Lorem ipsum - red", "qt": 1050, "price": "4.5"},
            {"id": "45", "name": "Lorem ipsum - black", "qt": 156, "price": "4.5"},
            {"id": "45", "name": "Lorem ipsum - white", "qt": 9, "price": "4.6"},
        ],
    }

    report = Q2Report()
    report.set_style(report.make_style(border_width="0"))
    report.add_page(page_margin_left=3, page_height=21, page_width=21)

    report.add_column(width=1)
    report.add_column(width=3)
    report.add_column(width="50%")
    report.add_column()
    report.add_column()
    report.add_column()
    report.add_row(height="2-0")

    # report.set_cell(0, 0, "{q2image('%s')}" % image_data, colspan=2)
    report.set_cell(
        0,
        2,
        colspan=4,
        data="Invoice <b>{rep.d.invoice.number}<b>",
        style=report.make_style(font_size=20),
    )

    label_style = report.make_style(text_align="right", font_size=8, padding="0.05 0.5 0.05 0.05")

    report.set_cell(1, 0, colspan=2, data="Date of origin:", style=label_style)

    report.set_cell(1, 2, data="{rep.d.invoice.date}", format="D")
    report.set_cell(1, 4, data="Expiry date:", style=label_style)
    report.set_cell(1, 5, data="{rep.d.invoice.expire_date}", format="D")

    report.set_cell(2, 2, colspan=3, data="<b>{rep.d.supplier.name}</b>, ({rep.d.supplier.id})")
    report.set_cell(2, 0, colspan=2, data="Supplier", style=label_style)

    report.set_cell(3, 2, colspan=3, data="{rep.d.supplier.address}")

    report.set_cell(4, 0, colspan=2, data="Customer", style=label_style)
    report.set_cell(4, 2, colspan=3, data="<b>{rep.d.customer.name}</b>")
    report.set_cell(5, 2, colspan=3, data="{rep.d.customer.address}")

    report.set_cell(6, 0, colspan=2, data="Comments", style=label_style)
    report.set_cell(6, 2, colspan=3, data="<i>{rep.d.invoice.comments}</i>")

    # Table
    table_row = Q2Report_rows(
        role="table", data_source="items", style=report.make_style(border_width="0 0 1 0")
    )
    table_header = Q2Report_rows(style=report.make_style(text_align="center", border_width="1"))
    table_footer = Q2Report_rows()

    table_header.set_cell(
        0, 0, "Invoice items", colspan=7, style=report.make_style(border_width="0", font_size=12)
    )
    table_row.set_cell(0, 0, "{_row_number}.", style=report.make_style(text_align="center"))

    table_header.set_cell(1, 0, "Goods and Services", colspan=3)

    table_row.set_cell(0, 1, "<b>{name}</b>, ({id})", colspan=2)

    table_header.set_cell(1, 3, "Quantity")
    table_row.set_cell(0, 3, "{qt}", format="N", style=report.make_style(text_align="right"))
    table_footer.set_cell(0, 3, "Subtotal", colspan=2, style=label_style)
    table_footer.set_cell(1, 3, "Discount", colspan=2, style=label_style)
    table_footer.set_cell(2, 3, "Discount amount", colspan=2, style=label_style)
    table_footer.set_cell(3, 3, "Grand total", colspan=2, style=label_style)

    table_header.set_cell(1, 4, "Price")
    table_row.set_cell(0, 4, "{price}", format="$N2", style=report.make_style(text_align="right"))

    table_header.set_cell(1, 5, "Total")
    table_row.set_cell(
        0,
        5,
        "{num(price)*num(qt)}",
        format="F2$",
        style=report.make_style(text_align="right"),
        name="line_total",
    )
    table_footer.set_cell(
        0,
        5,
        "{sum:num(line_total)}",
        format="F",
        style=report.make_style(text_align="right", font_weight="bold"),
        name="sub_total",
    )
    table_footer.set_cell(
        1,
        5,
        "{rep.d.invoice.discount}",
        style=report.make_style(text_align="right", font_weight="bold"),
        name="discount",
    )
    table_footer.set_cell(
        2,
        5,
        "{-round(num(sub_total)*num(discount)/100,2)}",
        style=report.make_style(text_align="right", font_weight="bold"),
        format="F",
        name="discount_amount",
    )
    table_footer.set_cell(
        3,
        5,
        "{num(sub_total)+num(discount_amount)}",
        style=report.make_style(text_align="right", font_weight="bold"),
        format="F",
        name="grand_total",
    )

    table_row.set_table_header(table_header)
    table_row.set_table_footer(table_footer)

    report.add_rows(rows=table_row)

    # res_file = report.run("temp/repo.html", data=demo_data, open_output_file=False)
    res_file = report.run("temp/repo.xlsx", data=demo_data, open_output_file=False)
    # res_file = report.run("temp/repo.docx", data=demo_data, open_output_file=False)

    os.system(os.path.abspath(res_file))


if __name__ == "__main__":  # pragma: no cover
    demo()
