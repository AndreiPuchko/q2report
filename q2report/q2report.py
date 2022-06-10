if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")
    from demo.demo_00 import demo

    demo()


import json
from copy import deepcopy
import re
from q2report.q2printer.q2printer import Q2Printer, get_printer
from q2report.q2utils import num

re_calc = re.compile(r"\{.*?\}")

engine_name = None


def set_engine(engine2="PyQt6"):
    global engine
    engine = engine2


class mydata(dict):
    def __init__(self, q2report):
        super().__init__()
        self.q2report = q2report

    def __getitem__(self, key):
        if self.q2report.use_prevrowdata:
            data = self.q2report.prevrowdata
        else:
            data = self.q2report.data
        if key in data:
            return data[key]
        elif key in globals():
            return globals()[key]
        else:
            return ""


class Q2Report:
    def __init__(self):
        self.report_data = None
        self.data_sources = {}
        self.printer = None
        self.data = {}
        self.prevrowdata = {}
        self.use_prevrowdata = False
        self.mydata = mydata(self)
        self.table_aggregators = {}
        self.table_group_aggregators = []
        self.outline_level = 0

    def load(self, content):
        self.report_data = json.load(open(content))

    def formulator(self, formula):
        formula = formula[0][1:-1]
        if self.use_prevrowdata:
            data = self.prevrowdata
        else:
            data = self.data
        if formula in data:
            return str(data[formula])
        else:
            return self.evaluator(formula)

    def evaluator(self, formula):
        try:
            rez = str(eval(formula, self.mydata))
        except BaseException:
            rez = f"Evaluating error: {formula}"
        return rez

    def render_rows_section(self, rows_data, row_style, aggregator=None):
        if aggregator is None:
            self.use_prevrowdata = False
            self.data.update({x: self.table_aggregators[x]["v"] for x in self.table_aggregators})
        else:
            self.prevrowdata.update({x: aggregator[x]["v"] for x in aggregator})
            self.use_prevrowdata = True
        rows_data = deepcopy(rows_data)
        for cell in rows_data["cells"]:
            cell_data = rows_data["cells"][cell].get("data")
            if cell_data and re_calc.findall(cell_data):
                rows_data["cells"][cell]["data"] = re_calc.sub(self.formulator, cell_data)

        row_style = dict(row_style)
        row_style.update(rows_data.get("style", {}))
        self.printer.render_rows_section(rows_data, row_style, self.outline_level)

    def run(self, output_file="tmp/repo.html", output_type=None, data={}):
        self.printer: Q2Printer = get_printer(output_file, output_type)
        report_style = dict(self.report_data["style"])

        for page in self.report_data.get("pages", []):
            page_style = dict(report_style)
            page_style.update(page.get("style", {}))
            self.printer.reset_page(**{x: page[x] for x in page if x.startswith("page_")})

            for column in page.get("columns", []):
                column_style = dict(page_style)
                column_style.update(column.get("style", {}))
                self.printer.reset_columns(column["widths"])

                for rows_data in column.get("rows", []):
                    data_set = data.get(rows_data["data_source"], [])
                    if rows_data["role"] == "table" and data_set != []:
                        # table rows
                        self.aggregators_reset(rows_data)
                        self.data["_row_count"] = len(data_set)

                        self.render_table_header(rows_data, column_style)
                        for data_set_row_number in range(len(data_set)):
                            self.data["_row_number"] = data_set_row_number + 1
                            self.data.update(data_set[data_set_row_number])

                            self.render_table_groups(rows_data, column_style)
                            self.aggregators_calc()
                            self.outline_level += 1
                            self.render_rows_section(rows_data, column_style)
                            self.outline_level -= 1
                            self.prevrowdata.update(data_set[data_set_row_number])

                        self.render_table_groups(rows_data, column_style, True)
                        self.render_table_footer(rows_data, column_style)
                    else:  # Free rows
                        self.render_rows_section(rows_data, column_style)

        self.printer.save()
        self.printer.show()

    def render_table_header(self, rows_data, column_style):
        if rows_data.get("table_header"):
            self.render_rows_section(rows_data["table_header"], column_style)

    def render_table_groups(self, rows_data, column_style, end_of_table=False):
        reset_index = None
        for index, group_set in enumerate(rows_data["table_groups"]):
            agg = self.table_group_aggregators[index]
            group_value = []
            for group in agg["groupby_list"]:
                group_value.append(self.evaluator(group))
            if agg["groupby_values"] != group_value and agg["groupby_values"] != [] or end_of_table:
                reset_index = index
                break
        if reset_index is not None:
            for index in range(len(rows_data["table_groups"]) - 1, index - 1, -1):
                agg = self.table_group_aggregators[index]
                self.render_rows_section(
                    rows_data["table_groups"][index]["group_footer"],
                    column_style,
                    aggregator=agg["aggr"],
                )
                self.outline_level -= 1
                # clear group aggregator
                agg["groupby_values"] = []
                for cell in agg["aggr"]:
                    agg["aggr"][cell]["v"] = num(0)
                agg["aggr"]["_row_number"]["v"] = num(0)
        if end_of_table:
            return
        for index, group_set in enumerate(rows_data["table_groups"]):
            agg = self.table_group_aggregators[index]
            group_value = []
            for group in agg["groupby_list"]:
                group_value.append(self.evaluator(group))
            if agg["groupby_values"] != group_value:
                self.outline_level += 1
                self.render_rows_section(group_set["group_header"], column_style)

    def render_table_footer(self, rows_data, column_style):
        if rows_data.get("table_footer"):
            self.render_rows_section(rows_data["table_footer"], column_style)

    def aggregators_detect(self, rows_data, aggregator):
        formulas = []
        for cell_data in rows_data.get("cells").items():
            cell_data = cell_data[1].get("data")
            for x in re_calc.findall(cell_data):
                f = x[1:-1]
                if f not in formulas:
                    formulas.append(f)
        for cell_data in formulas:
            for mode in ["sum"]:
                if cell_data.lower().startswith(f"{mode}:"):
                    aggregator[cell_data] = {
                        "a": mode,  # aggregate function - sum, avg and etc
                        "f": cell_data[1 + len(mode) :],  # cell formula  # noqa: E203
                        "v": num(0),  # initial value
                    }

        aggregator["_row_number"] = {
            "a": mode,  # aggregate function - sum, avg and etc
            "f": "",  # cell formula
            "v": num(0),  # initial value
        }

    def aggregators_reset(self, rows_data):
        self.table_aggregators = {}
        self.table_group_aggregators = []
        self.aggregators_detect(rows_data.get("table_footer", {}), self.table_aggregators)
        grouper = []
        for group in rows_data["table_groups"]:
            grouper.append(group["group_footer"]["groupby"])
            aggr = {
                "groupby_list": grouper[:],
                "groupby_values": [],
                "aggr": {},
            }
            self.aggregators_detect(group.get("group_footer", {}), aggr["aggr"])
            self.table_group_aggregators.append(aggr)

    def aggregators_calc(self):
        for y, x in self.table_aggregators.items():
            x["v"] += num(self.evaluator(x["f"]))

        for x in self.table_group_aggregators:
            x["groupby_values"] = []
            for y in x["groupby_list"]:
                x["groupby_values"].append(self.evaluator(y))
            # x["last_row_data"] = deepcopy(self.data)
            for cell in x["aggr"]:
                x["aggr"][cell]["v"] += num(self.evaluator(x["aggr"][cell]["f"]))
            x["aggr"]["_row_number"]["v"] += 1