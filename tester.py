#!/usr/bin/env python3
import sys

import pybud

num_list = [500, 600, 700]
alpha_list = ['x', 'y', 'z']


def sample(a, b):
    x = a + b
    y = x * 2
    print('Sample: ' + str(y))


def nested_loop():
    for number in num_list:
        print(number)
        for letter in alpha_list:
            print(letter)


sys.settrace(pybud.trace_calls)

if __name__ == '__main__':
    sample(3, 2)
