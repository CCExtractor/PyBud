#!/usr/bin/env python3
import copy
import io
import sys
import time

from pybud import json_helper
from pybud.DiffFinder import DiffFinder


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
        self.print_log = []
        self.stdout_buffer = io.StringIO()
        self.last_stdout_len = 0
        self.Differ = DiffFinder()

    def reset(self):
        self.func_path = None
        self.steps = {}
        self.step = 1
        self.cached_vars = {}
        self.vars_log = {}
        self.lines_log = {}
        self.print_log = []
        self.stdout_buffer = io.StringIO()
        self.last_stdout_len = 0

    def run_debug(self, output_path, function, args):
        """
        Runs the passed python function with PyBud debugging.

        Parameters:
            :param output_path: where to output json
            :param function: The function to debug.
            :param args: The arguments you wish to pass to the function, in tuple format ie. '("one", 2, 4).
        """
        self.reset()
        self.func_name = function.__name__

        # capture stdout
        real_stdout = sys.stdout
        sys.stdout = self.stdout_buffer

        sys.settrace(self.trace_calls)
        self.ex_time = self.lst_time = time.time_ns()  # log start time

        ret = function(*args)  # call the method
        sys.settrace(None)  # turn off debug tracing after function finish
        self.ex_time = time.time_ns() - self.ex_time  # calculate time spent executing function

        # release stdout
        sys.stdout = real_stdout

        output = dict()  # create output

        output["func_name"] = self.func_name
        output["func_path"] = self.func_path
        output["passed_args"] = args
        output["ex_time"] = self.ex_time
        output["steps"] = self.steps
        output["vars_log"] = self.vars_log
        output["lines_log"] = self.lines_log
        output["print_log"] = self.print_log

        # save the dict to a file as json
        json_helper.dict_to_json_file(output, output_path)

        return ret  # return the function's response

    def trace_calls(self, frame, event, arg):
        co = frame.f_code  # ref to code object
        self.line = frame.f_lineno  # initialize line number before we start debugging the lines
        if self.func_name == co.co_name:  # check if in desired function
            self.func_path = co.co_filename
            return self.trace_lines

    def trace_lines(self, frame, event, arg):
        # immediately log the change in time since last step/line
        diff = time.time_ns() - self.lst_time

        # TODO: tree printfs instead of capturing them
        this_out = self.stdout_buffer.getvalue()
        new_out = this_out[self.last_stdout_len:].rstrip("\n")
        if new_out:
            self.print_log.append({"step": self.step, "print": new_out})
        self.last_stdout_len = len(this_out)

        this_step = self.steps[self.step] = dict()
        this_step["ts"] = time.time()  # log timestamp for this step
        if self.line not in self.lines_log:
            self.lines_log[self.line] = {"cnt": 0, "total": 0.0}
        self.lines_log[self.line]["total"] += diff
        self.lines_log[self.line]["cnt"] += 1

        line = {"num": self.line, "total": self.lines_log[self.line]["total"], "cnt": self.lines_log[self.line]["cnt"]}
        this_step["line"] = line  # log line data for this step

        # init events key
        this_step["events"] = {"var_inits": [], "var_changes": []}

        local_vars = frame.f_locals  # grab variables from frame
        for v, val in local_vars.items():
            if v not in self.cached_vars:  # variable is not yet tracked, initialize and log
                this_step["events"]["var_inits"].append(self.var_initialize(v, copy.deepcopy(val)))
            else:
                # check if the variable has changed
                is_changed, events = self.Differ.evaluate_diff(v, self.cached_vars[v], copy.deepcopy(local_vars[v]))
                if is_changed:
                    this_step["events"]["var_changes"].extend(events.copy())
                    self.var_change(v, copy.deepcopy(val))  # add change to variable change log
                    self.cached_vars[v] = copy.deepcopy(val)  # update value of variable in local store

        self.line = frame.f_lineno  # update line number for next run
        self.lst_time = time.time_ns()  # update time for next run
        self.step += 1  # increment step

    def var_initialize(self, new_var, value) -> dict:
        self.cached_vars[new_var] = copy.deepcopy(value)
        var_type = type(value).__name__  # get name of variable type without <class> tag
        # Create event data for this variable w/ line
        event = {"name": new_var, "type": var_type, "val": value, "line": self.line, "step": self.step}
        # Initialize variable in variable log
        if type(value) in [int, float]:
            self.vars_log[new_var] = {"init": event, "changes": [], "min": value, "max": value}
        else:
            self.vars_log[new_var] = {"init": event, "changes": []}
        # log init as a change
        self.var_change(new_var, value)
        return {"name": new_var, "type": var_type, "val": value}  # Return event data for this variable w/o line

    def var_change(self, var, new_val):
        var_key = self.vars_log[var]
        var_key["changes"].append({"step": self.step, "line": self.line, "val": new_val})
        if "min" in var_key:  # this is a variable with min and max tracking
            var_key["min"] = min(new_val, var_key["min"])
            var_key["max"] = max(new_val, var_key["max"])
