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

def trace_changes(frame, event, arg):

    def trace_calls(self, frame, event, arg):
        co = frame.f_code  # ref to code object
        self.line = frame.f_lineno  # initialize line number before we start debugging the lines
        if self.func_name == (curr_fun := co.co_name):  # check if in desired function
            print("Debugging the " + curr_fun + " function in the file " + co.co_filename + " ...")
            return self.trace_lines

    def trace_lines(self, frame, event, arg):
        local_vars = frame.f_locals

        for v in local_vars:
            changed = True
            if v not in self.cached_vars:  # variable is not yet locally tracked
                variable_init(self.line, v, local_vars[v])
                self.initialize_var(v, local_vars[v])
                changed = False
            elif isinstance(local_vars[v], Sequence) and not isinstance(local_vars[v], str):
                # check if current variable is a Sequence type (ie. list, tuple, etc.), has changed, and is NOT a string
                changed = False
                for i, (new, old) in enumerate(zip_longest(local_vars[v], self.cached_vars[v])):
                    if new != old:  # an item  in this Sequence variable has been modified in some way
                        if old is None:  # item added
                            seq_item_added(self.line, v, i, new)
                        elif new is None:  # item removed
                            seq_item_removed(self.line, v, i, old)
                        else:  # item changed
                            seq_item_change(self.line, v, i, old, new)
                        changed = True

            else:
                if local_vars[v] != self.cached_vars[v]:
                    variable_value_change(self.line, v, self.cached_vars[v], local_vars[v])
            if changed:
                self.cached_vars[v] = local_vars[v]  # update value of variable in local store

        self.line = frame.f_lineno  # update line number for next run

    def initialize_var(self, new_var, value):
        self.cached_vars[new_var] = value


def initialize_local_value(new_var, value):
    values[new_var] = value
