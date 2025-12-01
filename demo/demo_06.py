from q2report import Q2Report
import json
import os


def demo(type="pdf"):
    report = Q2Report()
    report.load(open("test_data/test-report-03.json").read())
    data = json.load(open("test_data/test-data-03.json"))
    res_file = report.run(f"temp/repo.{type}", data=data, open_output_file=1)


if __name__ == "__main__":  # pragma: no cover
    demo()
