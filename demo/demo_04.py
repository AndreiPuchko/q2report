from q2report import Q2Report
import json
import os


def demo(type="pdf", open_output_file=True):
    report = Q2Report()
    report.load(open("test_data/test-report-01.json").read())
    report.run(
        f"temp/repo.{type}",
        data=json.load(open("test_data/test-data-01.json")),
        open_output_file=open_output_file,
    )


if __name__ == "__main__":  # pragma: no cover
    demo()
