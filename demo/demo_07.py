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
                            "data_source": "lines",
                            "groupby": "",
                            "table_groups": [],
                            "print_when": "",
                            "print_after": "",
                            "style": {"border-width": "1 1 1 1"},
                            "new_page_before": "",
                            "new_page_after": "",
                            "heights": ["0-0"],
                            "cells": {
                                "0,0": {"data": "{line_number}"},
                                "0,1": {
                                    "data": "{name}<br><font size=-1>{description}</font>",
                                    "rowspan": 1,
                                    "colspan": 6,
                                },
                                "0,7": {
                                    "data": "{quantity}",
                                    "style": {"text-align": "right"},
                                    "format": "N4",
                                },
                                "0,8": {
                                    "data": "{net_price}",
                                    "style": {"text-align": "right"},
                                    "format": "N2",
                                },
                                "0,9": {
                                    "data": "{vat_rate}",
                                    "style": {"text-align": "right"},
                                    "format": "N2",
                                },
                                "0,10": {
                                    "data": "{net_total}",
                                    "format": "F2",
                                    "style": {"text-align": "right"},
                                },
                            },
                        }
                    ],
                    "widths": ["0.00", "0.00", "0.00", "0", "0", "0", "0.00", "2.00", "3.00", "2.00", "2.50"],
                }
            ],
            "page_width": 21.0,
            "page_height": 29.0,
            "page_margin_left": 2.0,
            "page_margin_top": 2.0,
            "page_margin_right": 1.0,
            "page_margin_bottom": 2.0,
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
            "line_number": "1",
            "description": "Rolle Netzwerkkabel, 100 Meter.",
            "quantity": "333.0000",
            "unit_code": "",
            "net_price": "55.0000",
            "net_total": "18315.00",
            "vat_rate": "7.00",
            "name": "Netzwerkkabel Cat 6 (100m)",
        },
    ]
}


def demo(type="pdf"):
    report = Q2Report()
    report.load(report_content)
    report.run(f"temp/repo.{type}", data=report_data, open_output_file=1)


if __name__ == "__main__":  # pragma: no cover
    demo()
