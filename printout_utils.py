#!/usr/bin/env python3


def variable_init(line, variable, value):
    print("Line {}:> variable '{}' was initialized to '{}'".format(line, variable, value))


def variable_value_change(line, variable, old_val, new_val):
    print("Line {}:> variable '{}' changed from '{}' to '{}'".format(line, variable, old_val, new_val))


def seq_item_added(line, variable, index, value):
    print("Line {}:> variable '{}': sequence item with value '{}' was added at index '{}'"
          .format(line, variable, value, index))


def seq_item_removed(line, variable, index, value):
    print("Line {}:> variable '{}': sequence item at index '{}' with value '{}' was removed"
          .format(line, variable, index, value))


def seq_item_change(line, variable, index, old_val, new_val):
    print("Line {}:> variable '{}': sequence item at index '{}' changed from '{}' to '{}'"
          .format(line, variable, index, old_val, new_val))
