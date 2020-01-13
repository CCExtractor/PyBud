#!/usr/bin/env python3
import inspect
from collections import Sequence
from itertools import zip_longest

from printout_utils import *

global values
values = {}


def trace_calls(frame, event, arg):
    # ref to code object and source
    co = frame.f_code
    source = inspect.getsourcelines(co)[0]

    print("Currently in the " + co.co_filename + " file and the " + co.co_name + " function")

    return trace_changes


def trace_changes(frame, event, arg):
    variables = frame.f_code.co_varnames
    local_vars = frame.f_locals

    for v in local_vars:
        changed = True
        if v not in values:  # variable is not yet locally tracked
            variable_init(frame.f_lineno - 1, v, local_vars[v])
            initialize_local_value(v, local_vars[v])
            changed = False
        elif isinstance(local_vars[v], Sequence) and not isinstance(local_vars[v], str):
            # check if current variable is a Sequence type (ie. list, tuple, etc.), has changed, and is NOT a string
            changed = False
            for i, (new, old) in enumerate(zip_longest(local_vars[v], values[v])):
                if new != old:  # an item  in this Sequence variable has been modified in some way
                    if old is None:  # item added
                        print("item added ", new)
                        # values[v].insert(i, new)
                    elif new is None:  # item removed
                        print("item removed ", old)
                        # values[v].pop(i)
                    else:  # item changed
                        print("item changed ", old, " ", new)
                    changed = True

        else:
            if local_vars[v] != values[v]:
                variable_value_change(frame.f_lineno - 1, v, values[v], local_vars[v])
        if changed:
            values[v] = local_vars[v]  # update value of variable in local store


def initialize_local_value(new_var, value):
    values[new_var] = value
