from q2report import Q2Report
import json
import os


def demo(type="pdf", open_output_file=True):
    report = Q2Report()
    report.load(open("test_data/test-report-02.json").read())
    # set data grouping
    report.report_content["pages"][0]["columns"][0]["rows"][0]["groupby"] = "tom, grp"

    data = json.load(open("test_data/test-data-02.json"))
    # sort dataset
    data["cursor"].sort(key=lambda r: (r["tom"], r["grp"]))

    report.run(f"temp/repo.{type}", data=data, open_output_file=open_output_file)


if __name__ == "__main__":  # pragma: no cover
    demo()
