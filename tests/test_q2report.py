import pytest
from unittest.mock import patch, mock_open
from q2report import __version__
from q2report.q2report import Q2Report


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


def test_report():
    report = Q2Report()
    report.load("test_data/report_02.json")
    report.params["p1"] = " <b>123</b> "

    with patch("builtins.open", mock_open()) as filemock:
        report.run("repo.docx", data=demo_data, open_output_file=False)
        report.run("repo.xlsx", data=demo_data, open_output_file=False)
        report.run("repo.html", data=demo_data, open_output_file=False)

    with pytest.raises(BaseException) as e:
        report.run("temp/repo.rtf", data=demo_data, open_output_file=False)


if __name__ == "__main__":
    test_report()
