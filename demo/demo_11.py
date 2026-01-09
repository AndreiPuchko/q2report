from q2report import Q2Report
import json

report_content = {
    "pages": [
        {
            "columns": [
                {
                    "rows": [
                        {
                            "role": "table",
                            "data_source": "header",
                            "cells": {"0,1": {"data": "{initial_note}", "rowspan": 1, "colspan": 9}},
                            "style": {"font-size": "12pt", "border-width": "1 0 1 0"},
                            "groupby": "",
                            "table_groups": [],
                            "print_when": "",
                            "print_after": "",
                            "new_page_before": "",
                            "new_page_after": "",
                            "heights": ["0-0"],
                        }
                    ],
                    "widths": ["0.00", "0.00", "0.00", "0", "0", "0", "0.00", "2.00", "2.10", "2.00", "2.50"],
                }
            ],
            "page_width": "21.00",
            "page_height": "29.70",
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
            "curr_id": "978",
            "payment_terms_days": "14",
            "due_date": "2025-12-10",
            "delivery_date": "2025-12-01",
            "skonto_rate": "3.00",
            "skonto_days": "7",
            "skonto_due_date": "2025-12-03",
            "net_amount": "60445.00",
            "gross_amount": "67405.75",
            "initial_note": "cdsg vsgd f;hblkd\ndfhgdfg\nh dfg\u0432\u0432\u0432\nh df\ng\nh fdgbgsdflhkg 'sdflg ;sldk g;klsdgs",
            "closing_note": "c3402-580293485234523\n52 254\n23 9 23849523\nvdfbvsdfgbg sdfhg\n234sdfhgsdfhf\n523\n4523\n52\n3",
            "q2_time": "20260104095058",
            "q2_mode": "u",
            "q2_hidden": "",
            "q2_bcolor": "0",
            "q2_fcolor": "0",
            "seller_name": "Webware Internet Solutions GmbH",
            "seller_street": "Einbahn Stra\u00dfe 19",
            "seller_postal_code": "12345",
            "seller_city": "Musterstadt",
            "seller_country_id": "DE",
            "seller_vat_id": "DE279247134",
            "seller_legal_id": "HRB 15635",
            "seller_tax_number": "262/481/0918",
            "seller_uri_id": "",
            "seller_commercial_register_court": "Amtsgericht Musterstadt",
            "seller_managing_director": "Dipl. -Kfm Ale Musterchef",
            "seller_phone": "+49 (0) 123 654 78 98",
            "seller_fax": "+49 (0) 123 654 44 33",
            "seller_email": "mustermail@mailmail.de",
            "seller_webpage": "wwis.de",
            "buyer_name": "Musterfirma GmbH",
            "buyer_street": "Musterstra\u00dfe 14",
            "buyer_postal_code": "54321",
            "buyer_city": "Musterstadt",
            "buyer_country_id": "DE",
            "buyer_vat_id": "",
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
