from q2report import Q2Report
import json
import os


def demo():
    report = Q2Report()
    report.load(open("test_data/test-report-02.json").read())
    report.report_content["pages"][0]["columns"][0]["rows"][0]["groupby"] = "tom, grp"

    data = json.load(open("test_data/test-data-02.json"))
    data["cursor"].sort(key=lambda r: (r["tom"], r["grp"]))

    res_file = report.run("temp/result.docx", data=data)
    os.system(os.path.abspath(res_file))


if __name__ == "__main__":  # pragma: no cover
    demo()
