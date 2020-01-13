#!/usr/bin/env python3


def variable_init(line, variable, value):
    print("Line {}: variable '{}' was initialized to '{}'".format(line, variable, value))


def variable_value_change(line, variable, old_val, new_val):
    print("Line {}: variable '{}' changed from '{}' to '{}'".format(line, variable, old_val, new_val))

