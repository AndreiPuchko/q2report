from q2report.q2report import Q2Report

import random
import string
import os


def demo():
    demo_data = {"cursor": []}

    for x in range(100):
        demo_data["cursor"].append(
            {
                "data1": "".join([random.choice(string.ascii_letters) for x in range(9)]),
                "num1": f"{random.randint(3,10)}",
                "grp": int(x / random.randint(6, 10)),
                "tom": int(random.randint(1, 2)),
            }
        )

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

    report = Q2Report()
    report.load("test_data/report_02.json")
    report.params["p1"] = " <b>123</b> "

    # report.run("temp/repo.html", data=demo_data)
    # report.run("temp/repo.xlsx", data=demo_data)
    res_file = report.run("temp/repo.docx", data=demo_data, open_output_file=False)
    os.system(os.path.abspath(res_file))

if __name__ == "__main__":
    demo()
