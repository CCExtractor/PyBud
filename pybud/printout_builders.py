#!/usr/bin/env python3
from pybud.utils import best_duration


def live_header(function, args, path):
    return "# Debugging the '{}' function with arguments '{}' in the file '{}' ... #".format(function, args, path)


def live_step(step):
    return "Step {}:".format(step)


def live_line(line, count, total):
    return "Line {} executed {} times, total time spent on line: {}, average time: {}".format(line, count, best_duration(total), best_duration(total / count))


def live_var_init(variable, value):
    return ":> variable '{}' was initialized to '{}'".format(variable, value)


def live_var_outer_change(variable, old_val, new_val):
    return ":> variable '{}' changed from '{}' to '{}'".format(variable, old_val, new_val)


def element_item_builder(path: list):
    item = "["
    for i, element in enumerate(path):
        if isinstance(element, int):
            item += str(element)
        else:
            item += "'" + element + "'"
        if i != len(path) - 1:
            item += "]["
        else:
            item += "]"
    return item


def live_var_item_change(variable, var_path, old_val, new_val):
    element = variable + element_item_builder(var_path)
    return ":> In variable '{}', the item '{}' changed from '{}' to '{}'".format(variable, element, old_val, new_val)


def live_var_item_add(variable, var_path, val):
    element = variable + element_item_builder(var_path)
    return ":> In variable '{}', the item '{}' was initialized to '{}'".format(variable, element, str(val))


def live_var_item_remove(variable, var_path, val):
    element = variable + element_item_builder(var_path)
    return ":> In variable '{}', the item '{}' was removed. It's value was: '{}'".format(variable, element, str(val))


def report_var_init(variable, var_type, step, value, line):
    return "Variable '{}' of type '{}' was initialized at step '{}' with value '{}' on line '{}'".format(variable, var_type, step, value, line)


def report_var_range(min_value, max_value):
    return "The range of the variable was: [{},{}]".format(min_value, max_value)


def report_changes(changes: list, length):
    ret = ""
    for i, change in enumerate(changes):
        if i != length - 1:
            ret += "line {}: '{}', ".format(change["line"], change["val"])
        else:
            ret += "line {}: '{}'".format(change["line"], change["val"])
    return "The variable changed on the following lines:\n" + ret


def report_final_value(value):
    return "The final value was: '{}'".format(value)


def report_exec_time(function, time):
    return "Total time spent executing '{}' function: {}".format(function, best_duration(time))


def report_line_exec(line, count, total):
    return "Line {} executed {} times, total time spent executing: {}".format(line, count, best_duration(total))


def vid_var_init(variable, var_type, value, line):
    return "Variable '{}' of type '{}' was initialized with value '{}' on line '{}'".format(variable, var_type, value, line)


def vid_history_up_to_step(changes: list, step):
    ret = ""
    this_change = None
    for i, change in enumerate(changes):
        if change["step"] == step:
            this_change = change["val"]
        elif change["step"] > step:
            break
        else:
            if i != len(changes) - 1:
                ret += "line {}: '{}', ".format(change["line"], change["val"])
            else:
                ret += "line {}: '{}'".format(change["line"], change["val"])
    return "History:\n" + ret, this_change


def vid_change_from_to(variable, old_val, new_val):
    return "Variable '{}': changed to '{}' from '{}'".format(variable, new_val, old_val)


def vid_variable(variable, val):
    return "Variable '{}': current value '{}'".format(variable, val)

