from q2report import Q2Report
import json
import os


def demo():
    report = Q2Report()
    report.load(open("test_data/test-report-03.json").read())
    data = json.load(open("test_data/test-data-03.json"))
    res_file = report.run("temp/result.pdf", data=data)
    os.system(os.path.abspath(res_file))


if __name__ == "__main__":  # pragma: no cover
    demo()
