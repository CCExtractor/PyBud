#!/usr/bin/env python3
import inspect

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
        if v not in values:
            ret = "Line {}: variable '{}' was initialized to {}" \
                .format(frame.f_lineno - 1, v, local_vars[v])
            print(ret)
            initialize_local_value(v, local_vars[v])
        if isinstance(local_vars[v], list):  # check if current variable is a list
            continue
            # print("DEBUG || is list")
        else:
            if local_vars[v] != values[v]:
                ret = "Line {}: variable '{}' changed from {} to {}" \
                    .format(frame.f_lineno - 1, v, values[v], local_vars[v])
                print(ret)
                values[v] = local_vars[v]  # update value of variable in local store


def initialize_local_value(new_var, value):
    values[new_var] = value
