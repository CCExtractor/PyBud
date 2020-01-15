#!/usr/bin/env python3
import sys
import time
from collections import Sequence
from itertools import zip_longest

from printout_utils import *


class PyBud:
    def __init__(self):
        self.func = None
        self.func_name = None
        self.line = None
        self.cached_vars = {}
        self.vars_log = {}
        self.lines_log = {}
        self.ex_time = None
        self.lst_time = None

    def run_debug(self, function, *args):
        """
        Runs the passed python function with PyBud debugging.

        Parameters:
            function: The function you wish to debug.
            args: The arguments you wish to pass to the function
        """
        self.func_name = function.__name__
        self.func = function

        sys.settrace(self.trace_calls)

        self.ex_time = self.lst_time = time.time() * 1000.0  # log start time
        function(*args)  # call the method
        self.ex_time = time.time() * 1000.0 - self.ex_time  # calculate time spent executing function

        self.print_log()  # printout end log

    def trace_calls(self, frame, event, arg):
        co = frame.f_code  # ref to code object
        self.line = frame.f_lineno  # initialize line number before we start debugging the lines
        if self.func_name == (curr_fun := co.co_name):  # check if in desired function
            print("\n# Debugging the " + curr_fun + " function in the file " + co.co_filename + " ... #\n")
            return self.trace_lines

    def trace_lines(self, frame, event, arg):
        diff = time.time() * 1000.0 - self.lst_time
        if self.line not in self.lines_log:
            self.lines_log[self.line] = {"cnt": 0, "total": 0.0}
        self.lines_log[self.line]["total"] += diff
        self.lines_log[self.line]["cnt"] += 1
        print(">> Line {} executed {} times, total time spent on line: {}ms, average time: {}ms <<"
              .format(self.line, self.lines_log[self.line]["cnt"],
                      self.lines_log[self.line]["total"],
                      self.lines_log[self.line]["total"] / self.lines_log[self.line]["cnt"]))

        local_vars = frame.f_locals

        for v in local_vars:
            if v not in self.cached_vars:  # variable is not yet locally tracked
                variable_init(self.line, v, local_vars[v])
                self.var_initialize(v, local_vars[v])
            elif local_vars[v] != self.cached_vars[v]:
                if isinstance(local_vars[v], Sequence) and not isinstance(local_vars[v], str):
                    # check if current variable is a Sequence type (ie. list, tuple, etc.) but NOT a string
                    for i, (new, old) in enumerate(zip_longest(local_vars[v], self.cached_vars[v])):
                        if new != old:  # an item  in this Sequence variable has been modified in some way
                            if old is None:  # item added
                                seq_item_added(self.line, v, i, new)
                            elif new is None:  # item removed
                                seq_item_removed(self.line, v, i, old)
                            else:  # item changed
                                seq_item_change(self.line, v, i, old, new)
                else:
                    variable_value_change(self.line, v, self.cached_vars[v], local_vars[v])
                self.var_change(v, local_vars[v])  # add change to variable change log
                self.cached_vars[v] = local_vars[v]  # update value of variable in local store

        self.line = frame.f_lineno  # update line number for next run
        self.lst_time = time.time() * 1000.0

    def var_initialize(self, new_var, value):
        self.cached_vars[new_var] = value
        var_type = type(value)
        log = "The variable '{}' of type {} was initialized to '{}' on line {}" \
            .format(new_var, var_type, value, self.line)

        if var_type in [int, float]:
            self.vars_log[new_var] = {"init": log, "changes": [], "min": value, "max": value}
        else:
            self.vars_log[new_var] = {"init": log, "changes": []}

    def var_change(self, var, new_val):
        var_key = self.vars_log[var]
        var_key["changes"].append(str(self.line) + ":> '" + str(new_val) + "'")
        if "min" in var_key:  # this is a variable with min and max tracking
            var_key["min"] = min(new_val, var_key["min"])
            var_key["max"] = max(new_val, var_key["max"])

    def print_log(self):
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
