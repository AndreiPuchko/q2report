from q2report import Q2Report
import json
import os


def demo():
    report = Q2Report()
    report.load(open("test_data/test-report-01.json").read())
    res_file = report.run("temp/result.docx", data=json.load(open("test_data/test-data-01.json")))
    
    os.system(os.path.abspath(res_file))


if __name__ == "__main__":  # pragma: no cover
    demo()
