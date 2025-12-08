from q2report import Q2Report
import json

report_content = {
    "queries": {
        "header": "select \n    i.*, \n    \r\n    bp.name as buyer_name\r\n    , bp.street as buyer_street\r\n    , bp.postal_code as buyer_postal_code\r\n    , bp.city as buyer_city\r\n    , bp.country_code as buyer_country_code\r\n    , bp.vat_id as buyer_vat_id\r\n    \r\n    , sp.name as seller_name\r\n    , sp.street as seller_street\r\n    , sp.postal_code as seller_postal_code\r\n    , sp.city as seller_city\r\n    , sp.country_code as seller_country_code\r\n    , sp.vat_id as seller_vat_id\r\n    \r\n    , cur.iso_code as currency_code\r\n    \nfrom invoices i\n\r\nleft join parties bp on i.buyer_id = bp.pid\nleft join parties sp on i.seller_id = sp.pid\nleft join currencies cur on i.currency_id = cur.cid\n\r\nwhere i.id = :id\n",
        "lines": "select \n  line_number, description, quantity, unit_code, net_price, net_total, vat_rate, name\nfrom invoice_lines\nwhere invoice_id = :id\norder by line_number",
        "vat_breakdown": "select vat_rate, tax_base_amount, tax_amount from vat_breakdown where invoice_id = :id order by vat_rate",
    },
    "params": {"id": "1"},
    "pages": [
        {
            "columns": [
                {
                    "rows": [
                        {
                            "role": "table",
                            "data_source": "header",
                            "cells": {
                                "1,0": {
                                    "data": "Absender (Verk\u00e4ufer):",
                                    "rowspan": 1,
                                    "colspan": 6,
                                    "style": {"font-weight": "bold", "padding": "0 0 0 2.5"},
                                },
                                "2,0": {
                                    "data": "{seller_name}",
                                    "rowspan": 1,
                                    "colspan": 6,
                                },
                                "3,0": {
                                    "data": "{seller_street}",
                                    "rowspan": 1,
                                    "colspan": 6,
                                },
                                "4,0": {
                                    "data": "{seller_postal_code} {seller_city}",
                                    "rowspan": 1,
                                    "colspan": 6,
                                },
                                "2,8": {"data": "Rechnungs-Nr.:"},
                                "3,8": {"data": "Datum:"},
                                "4,8": {"data": "Lieferdatum:"},
                                "1,7": {
                                    "data": "Rechnung",
                                    "style": {
                                        "font-weight": "bold",
                                        "text-align": "right",
                                    },
                                    "rowspan": 1,
                                    "colspan": 4,
                                },
                                "2,9": {
                                    "data": "{invoice_number}",
                                    "rowspan": 1,
                                    "colspan": 2,
                                    "style": {"text-align": "center"},
                                },
                                "3,9": {
                                    "data": "{invoice_date:D}",
                                    "rowspan": 1,
                                    "colspan": 2,
                                    "style": {"text-align": "center"},
                                },
                                "4,9": {
                                    "data": "{delivery_date:D}",
                                    "rowspan": 1,
                                    "colspan": 2,
                                    "style": {"text-align": "center"},
                                },
                                "6,0": {
                                    "data": "Kunde (Empf\u00e4nger):",
                                    "rowspan": 1,
                                    "colspan": 6,
                                    "style": {"font-weight": "bold"},
                                },
                                "9,0": {
                                    "data": "{buyer_postal_code} {buyer_city}",
                                    "rowspan": 1,
                                    "colspan": 6,
                                },
                                "7,0": {
                                    "data": "{buyer_name}",
                                    "rowspan": 1,
                                    "colspan": 6,
                                },
                                "8,0": {
                                    "data": "{buyer_street}",
                                    "rowspan": 1,
                                    "colspan": 6,
                                },
                                "11,1": {
                                    "data": "{initial_note}",
                                    "rowspan": 1,
                                    "colspan": 9,
                                },
                            },
                            "style": {"border-width": "1 1 1 1", "font-size": "14"},
                            "groupby": "",
                            "table_groups": [],
                            "print_when": "",
                            "print_after": "",
                            "new_page_before": "",
                            "new_page_after": "",
                            "heights": [
                                "0-0",
                                "0-5",
                                "0-0",
                                "0-0",
                                "0-0",
                                "1-0",
                                "0-0",
                                "0-0",
                                "0-0",
                                "0-0",
                                "0.20-0.20",
                                "0-0",
                            ],
                        },
                    ],
                    "widths": ["0.00", "0.00", "0.00", "0", "0", "0", "0.00", "2.00", "3.00", "2.00", "2.50"],
                }
            ],
            "page_width": "21.00",
            "page_height": "29.00",
            "page_margin_left": "2.00",
            "page_margin_top": "1.00",
            "page_margin_right": "1.00",
            "page_margin_bottom": "1.00",
        }
    ],
    "style": {
        "font-family": "Arial",
        "font-size": "10pt",
        "font-weight": "normal",
        "font-style": "",
        "text-decoration": "",
        "border-width": "0 0 0 0",
        "padding": "0.05cm 0.05cm 0.05cm 0.05cm",
        "background": "#FFFFFF",
        "color": "#000000",
        "border-color": "#000000",
        "text-align": "left",
        "vertical-align": "top",
    },
    "module": "#",
}


report_data = {
    "params": {":id": "1"},
    "header": [
        {
            "id": "1",
            "invoice_number": "INV-3035-11-103",
            "invoice_date": "2025-11-27",
            "seller_id": "1",
            "buyer_id": "2",
            "currency_id": "978",
            "payment_terms_days": "14",
            "due_date": "2025-12-10",
            "net_amount": "36630.00",
            "gross_amount": "41391.90",
            "q2_time": "20251204192141",
            "q2_mode": "u",
            "q2_hidden": "",
            "q2_bcolor": "0",
            "q2_fcolor": "0",
            "delivery_date": "2025-12-01",
            "skonto_rate": "3.00",
            "skonto_days": "7",
            "skonto_due_date": "2025-12-03",
            "skonto_amount": "15.35",
            "initial_note": "Einle itu\n\n\nngstext * 1",
            "closing_note": "Schlusstext * 2 line2rth ;erl jh o; ;ke ;hioej r;hioje;itrohj ;wioj ht;iodjfhgil'dgdgfh dfh gdfh",
            "buyer_name": "Agoratech",
            "buyer_street": "Teichstr. 14-16",
            "buyer_postal_code": "34130",
            "buyer_city": "Kassel",
            "buyer_country_code": "",
            "buyer_vat_id": "",
            "seller_name": "Webware Internet Solutions GmbH",
            "seller_street": "Einbahn Stra\u00dfe 19",
            "seller_postal_code": "12345",
            "seller_city": "Hremen",
            "seller_country_code": "",
            "seller_vat_id": "DE279247134",
            "currency_code": "EUR",
        }
    ],
    "lines": [
        {
            "line_number": "1",
            "description": "Rolle Netzwerkkabel, 100 Meter.",
            "quantity": "333.0000",
            "unit_code": "",
            "net_price": "55.0000",
            "net_total": "18315.00",
            "vat_rate": "19.00",
            "name": "Netzwerkkabel Cat 6 (100m)",
        },
        {
            "line_number": "2",
            "description": "Rolle Netzwerkkabel, 100 Meter.",
            "quantity": "333.0000",
            "unit_code": "",
            "net_price": "55.0000",
            "net_total": "18315.00",
            "vat_rate": "7.00",
            "name": "Netzwerkkabel Cat 6 (100m)",
        },
    ],
    "vat_breakdown": [
        {"vat_rate": "7.00", "tax_base_amount": "18315.00", "tax_amount": "1282.05"},
        {"vat_rate": "19.00", "tax_base_amount": "18315.00", "tax_amount": "3479.85"},
    ],
}


def demo(type="pdf", open_output_file=True):
    report = Q2Report()
    report.load(report_content)
    report.run(f"temp/repo.{type}", data=report_data, open_output_file=open_output_file)


if __name__ == "__main__":  # pragma: no cover
    demo()
