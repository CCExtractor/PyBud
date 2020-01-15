#!/usr/bin/env python3
import sys

from pybud import PyBud


def main():
    debugger = PyBud()
    debugger.run_debug(sample, 3, 2)
    # nested_loop()


def sample(a, b):
    """
    Test case 1
    """
    x = 8
    y = 14

    x = a + b
    y = x * 2
    print('Math test: ' + str(y))

    fl = 1.234

    a_string = "this is a string"

    num_list = [500, 600, 700]
    num_list = [500, 600, 700]
    num_list = [100, 200, 700, 800]

    num_list = [100, 700, 800]


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


if __name__ == '__main__':
    main()
