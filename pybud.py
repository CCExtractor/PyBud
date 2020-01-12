#!/usr/bin/env python3
import inspect
import sys

global values
values = {}


def trace_calls(frame, event, arg):
    # ref to code object and source
    co = frame.f_code
    source = inspect.getsourcelines(co)[0]

    print("Currently in the " + co.co_filename + " file and the " + co.co_name + " function")

    # initialize local variable store
    for value in frame.f_code.co_varnames:
        values[value] = None

    return trace_changes


def trace_changes(frame, event, arg):
    variables = frame.f_code.co_varnames
    local_vars = frame.f_locals

    for v in variables:
        if v in local_vars:
            if local_vars[v] != values[v]:
                ret = "DEBUG || Line {}: variable '{}' changed from {} to {}" \
                    .format(frame.f_lineno, v, values[v], local_vars[v])
                print(ret)
                values[v] = local_vars[v]  # update value of variable
