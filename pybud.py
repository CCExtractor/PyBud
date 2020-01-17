#!/usr/bin/env python3
import sys
import time

import json_helper
from DiffFinder import DiffFinder


class PyBud:
    def __init__(self):
        self.func_name = None
        self.func_path = None
        self.line = None
        self.cached_vars = {}
        self.step = 1
        self.steps = {}
        self.vars_log = {}
        self.lines_log = {}
        self.ex_time = None
        self.lst_time = None
        self.Differ = DiffFinder()

    def reset(self):
        self.steps = []
        self.step = 1

    def run_debug(self, function, *args):
        """
        Runs the passed python function with PyBud debugging.

        Parameters:
            function: The function you wish to debug.
            args: The arguments you wish to pass to the function
        """
        self.func_name = function.__name__

        sys.settrace(self.trace_calls)

        self.ex_time = self.lst_time = time.time() * 1000.0  # log start time
        function(*args)  # call the method
        self.ex_time = time.time() * 1000.0 - self.ex_time  # calculate time spent executing function

        output = dict()

        output["func_name"] = self.func_name
        output["func_path"] = self.func_path
        output["passed_args"] = args
        output["ex_time"] = self.ex_time
        output["steps"] = self.steps
        output["vars_log"] = self.vars_log
        output["lines_log"] = self.lines_log

        json_helper.dict_to_json_file(output, "output.json")

        self.print_log()  # printout end log

    def trace_calls(self, frame, event, arg):
        co = frame.f_code  # ref to code object
        self.line = frame.f_lineno  # initialize line number before we start debugging the lines
        if self.func_name == (curr_fun := co.co_name):  # check if in desired function
            self.func_path = co.co_filename
            print("\n# Debugging the " + curr_fun + " function in the file " + self.func_path + " ... #\n")
            return self.trace_lines

    def trace_lines(self, frame, event, arg):
        this_step = self.steps[self.step] = dict()
        diff = (ts := time.time()) * 1000.0 - self.lst_time
        this_step["ts"] = ts  # log timestamp for this step
        if self.line not in self.lines_log:
            self.lines_log[self.line] = {"cnt": 0, "total": 0.0}
        self.lines_log[self.line]["total"] += diff
        self.lines_log[self.line]["cnt"] += 1
        print(">> Line {} executed {} times, total time spent on line: {}ms, average time: {}ms <<"  # TODO: move this
              .format(self.line, self.lines_log[self.line]["cnt"],
                      self.lines_log[self.line]["total"],
                      self.lines_log[self.line]["total"] / self.lines_log[self.line]["cnt"]))

        line = {"num": self.line, "total": self.lines_log[self.line]["total"], "cnt": self.lines_log[self.line]["cnt"]}
        this_step["line"] = line  # log line data for this step

        this_step["events"] = {"var_inits": [], "var_changes": []}

        local_vars = frame.f_locals  # grab variables
        for v in local_vars:
            if v not in self.cached_vars:  # variable is not yet tracked, initialize and log
                this_step["events"]["var_inits"].append(self.var_initialize(v, local_vars[v]))
            else:
                # check if the variable has changed
                is_changed, events = self.Differ.evaluate_diff(v, self.cached_vars[v], local_vars[v]);
                if is_changed:
                    this_step["events"]["var_changes"].extend(events.copy())
                    self.var_change(v, local_vars[v])  # add change to variable change log
                    self.cached_vars[v] = local_vars[v]  # update value of variable in local store

        self.line = frame.f_lineno  # update line number for next run
        self.lst_time = time.time() * 1000.0  # update time for next run
        self.step += 1  # increment step

    def var_initialize(self, new_var, value) -> dict:
        self.cached_vars[new_var] = value
        var_type = type(value)
        # Create event data for this variable
        event = {"name": new_var, "type": var_type, "val": value, "line": self.line}
        # Initialize variable in variable log
        if var_type in [int, float]:
            self.vars_log[new_var] = {"init": event, "changes": [], "min": value, "max": value}
        else:
            self.vars_log[new_var] = {"init": event, "changes": []}
        return event

    def var_change(self, var, new_val):
        var_key = self.vars_log[var]
        var_key["changes"].append({"line": self.line, "val": new_val})
        if "min" in var_key:  # this is a variable with min and max tracking
            var_key["min"] = min(new_val, var_key["min"])
            var_key["max"] = max(new_val, var_key["max"])

    def print_log(self):  # FIXME
        print("\n------------Debug finished, variable log:------------")

        for var, var_contents in self.vars_log.items():
            print("\n" + var_contents["init"])
            if "min" in var_contents:
                print("The range of the variable was: [{},{}]".format(var_contents["min"], var_contents["max"]))
            if (c_len := len(var_contents["changes"])) != 0:
                ret = ""
                for i, change in enumerate(var_contents["changes"]):
                    if i != c_len - 1:
                        ret += change + ", "
                    else:
                        ret += change
                print("Variable changed on the following lines: " + ret)
            print("The final value was: '{}'".format(self.cached_vars[var]))

        print("\n------------Execution time log:------------")

        print("Total time spent executing '{}' function: {}ms\n".format(self.func_name, self.ex_time))

        for line, line_contents in self.lines_log.items():
            print("Line {} executed {} times".format(line, line_contents["cnt"]))
