#!/usr/bin/env python3
import sys

import pybud


def sample(a, b):
    """
    Test case 1
    """
    x = a + b
    y = x * 2
    print('Sample: ' + str(y))


def nested_loop():
    """
        Test case 2
    """
    num_list = [500, 600, 700]
    alpha_list = ['x', 'y', 'z']

    for number in num_list:
        print(number)
        for letter in alpha_list:
            print(letter)


sys.settrace(pybud.trace_calls)

if __name__ == '__main__':
    sample(3, 2)
    # nested_loop()
