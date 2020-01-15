#!/usr/bin/env python3
import sys
from collections import Sequence
from itertools import zip_longest

from printout_utils import *


class PyBud:
    def __init__(self):
        self.func = None
        self.func_name = None
        self.cached_vars = {}
        self.line = None
        self.vars_log = {}

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

        function(*args)  # call the method

        self.print_log()

    def trace_calls(self, frame, event, arg):
        co = frame.f_code  # ref to code object
        self.line = frame.f_lineno  # initialize line number before we start debugging the lines
        if self.func_name == (curr_fun := co.co_name):  # check if in desired function
            print("Debugging the " + curr_fun + " function in the file " + co.co_filename + " ...")
            return self.trace_lines

    def trace_lines(self, frame, event, arg):
        local_vars = frame.f_locals

        for v in local_vars:
            if v not in self.cached_vars:  # variable is not yet locally tracked
                variable_init(self.line, v, local_vars[v])
                self.initialize_var(v, local_vars[v])
            elif local_vars[v] != self.cached_vars[v]:
                if isinstance(local_vars[v], Sequence) and not isinstance(local_vars[v], str):
                    # check if current variable is a Sequence type (ie. list, tuple, etc.) but is NOT a string
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
                self.var_changed(v, local_vars[v])  # add change to variable change log
                self.cached_vars[v] = local_vars[v]  # update value of variable in local store

        self.line = frame.f_lineno  # update line number for next run

    def initialize_var(self, new_var, value):
        self.cached_vars[new_var] = value
        var_type = type(value)
        log = "The variable '{}' of type {} was initialized to '{}' on line {}" \
            .format(new_var, var_type, value, self.line)

        self.vars_log[new_var] = dict()
        if var_type in [int, float]:
            self.vars_log[new_var] = {"init": log, "changes": [], "min": value, "max": value}
        else:
            self.vars_log[new_var] = {"init": log, "changes": []}

    def var_changed(self, var, new_val):
        var_key = self.vars_log[var]
        var_key["changes"].append(str(self.line) + ":> '" + str(new_val) + "'")
        if "min" in var_key:
            var_key["min"] = min(new_val, var_key["min"])
            var_key["max"] = max(new_val, var_key["max"])

    def print_log(self):
        print("\n------------Debug finished, printing log...------------")

        for var in self.vars_log.values():
            print("\n" + var["init"])
            if "min" in var:
                print("The range of the variable was: [" + str(var["min"]) + "," + str(var["max"]) + "]")
            if (c_len := len(var["changes"])) != 0:
                ret = ""
                for i, change in enumerate(var["changes"]):
                    if i != c_len - 1:
                        ret += change + ", "
                    else:
                        ret += change
                print("Variable changed on the following lines: " + ret)
