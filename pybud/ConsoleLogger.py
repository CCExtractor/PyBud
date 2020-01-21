import os

from pybud import json_helper
from pybud.printout_builders import *
from pybud.utils import *


class ConsoleLogger:
    def __init__(self, file_path):
        self.file_path = file_path

    def print_log(self):
        # parse json log file into dict
        log: dict = json_helper.json_file_to_dict(self.file_path)

        self.print_livetrace(log)
        self.print_end_summary(log)

    def print_livetrace(self, log: dict):
        # log livetrace header
        prYellow("\n" + live_header(log["func_name"], log["passed_args"], log["func_path"]))

        # read in program steps
        steps: dict = log["steps"]
        for step, step_contents in steps.items():
            # log this step
            prLightPurple("\n" + live_step(step), "")

            # log this line
            line: dict = step_contents["line"]
            prCyan(live_line(line["num"], line["cnt"], line["total"]))

            # read in events
            var_inits: list = step_contents["events"]["var_inits"]
            var_changes: list = step_contents["events"]["var_changes"]

            # log variable initializations
            for init in var_inits:
                prGreen(live_var_init(init["name"], init["val"]))

            # log variable changes
            for change in var_changes:
                str_chg = ""  # init local variable to store change message
                if change["type"] == "change":  # variable has changed
                    if len(change["var_path"]) == 0:  # this is an variable with no elements
                        str_chg = live_var_outer_change(change["var_name"], change["old_val"], change["new_val"])
                    else:  # an element in the variable changed
                        str_chg = live_var_item_change(change["var_name"], change["var_path"], change["old_val"],
                                                       change["new_val"])
                elif change["type"] == "add":  # variable has been added
                    path = list()
                    if len(change["var_path"]) == 0:  # there is no subpath to added element
                        path.append(change["element"])
                        str_chg = live_var_item_add(change["var_name"], path, change["new_val"])
                    else:  # there is a subpath to added element
                        path.append(change["var_path"])
                        path.append(change["element"])
                        str_chg = live_var_item_add(change["var_name"], path, change["new_val"])
                elif change["type"] == "remove":  # variable has been removed
                    path = list()
                    if len(change["var_path"]) == 0:  # there is no subpath to added element
                        path.append(change["element"])
                        str_chg = live_var_item_remove(change["var_name"], path, change["old_val"])
                    else:  # there is a subpath to added element
                        path.append(change["var_path"])
                        path.append(change["element"])
                        str_chg = live_var_item_remove(change["var_name"], path, change["old_val"])
                # log this variable change
                prGreen(str_chg)

    def print_end_summary(self, log):
        prPurple("\n------------Debug livetrace finished, variable log:------------")

        # read in variable log
        vars_log: dict = log["vars_log"]
        for var, var_contents in vars_log.items():
            # log the init props for this variable
            var_init: dict = var_contents["init"]
            prCyan("\n" + report_var_init(var_init["name"], var_init["type"], var_init["step"], var_init["val"], var_init["line"]))

            # check if this variable has minimum, maximum logging
            if "min" in var_contents:
                # log the range of this variable
                prGreen(report_var_range(var_contents["min"], var_contents["max"]))

            # init final value from this variable's initial value
            final_value = var_init["val"]
            if (c_len := len(var_contents["changes"])) != 0:
                final_value = var_contents["changes"][c_len - 1]["val"]  # define final value as value of last change
                # log the changes of this variable
                if c_len != 1:
                    prGreen(report_changes(var_contents["changes"], c_len))
            # log the final value of this variable
            prGreen(report_final_value(final_value))

        prPurple("\n------------Execution time log:------------")

        # log total execution time of the function
        prCyan(report_exec_time(log["func_name"], log["ex_time"]) + "\n")

        # log line execution data
        for line, line_contents in log["lines_log"].items():
            prGreen(report_line_exec(line, line_contents["cnt"], line_contents["total"]))
