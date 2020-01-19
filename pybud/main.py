#!/usr/bin/env python3
import argparse
import importlib
from pathlib import Path

from pybud.ConsoleLogger import ConsoleLogger
from pybud.PyBud import PyBud
from pybud.VideoLogger import VideoLogger
from pybud.example import sample
from pybud.tests.perform_tests import run_tests


def parse_args():
    parser = argparse.ArgumentParser(
        description="A Python debugger for analyzing and profiling functions. Created by Eastan Giebler."
    )

    debugging = parser.add_argument_group(title="Debugging",
                                          description="Debug a python function and generate an output log.")
    debugging.add_argument(
        "-d",
        "--debug",
        type=str,
        metavar="FILE",
        help="Path to the Python file you wish to debug."
    )

    debugging.add_argument(
        "-f",
        "--function",
        default="main",
        nargs="+",
        help="The function in the Python file you wish to debug, along with the arguments you wish to pass. "
             "Defaults to the main function if argument not used. "
             "EXAMPLE: '--function test 2 4' will call 'test(2,4)'."
    )

    debugging.add_argument(
        "-v",
        "--video",
        action="store_true",
        help="Generate a video rendering for the PyBud debug steps of the program flow. "
             " "
    )

    debugging.add_argument(
        "-o",
        "--output",
        default="output.pybud",
        metavar="FILE",
        help="Optional: Path to write the json log file. Defaults to output.pybud if argument not used."
    )

    parsing = parser.add_argument_group(title="Parsing and Analysis",
                                        description="Parse a PyBud JSON output and display to console in human-readable form.")
    parsing.add_argument(
        "-p",
        "--parse",
        nargs='?',
        const="output.pybud",
        metavar="FILE",
        help="Path to the json log you wish to parse into human-readable form. Defaults to output.pybud if a file is not specified."
    )

    parsing.add_argument(
        "-t",
        "--test",
        action="store_true",
        help="Test PyBud on a suite of sorting, searching, and similar algorithms. "
             "Outputs a PyBud JSON for each function in the 'test/test_logs' package. "
    )

    return parser.parse_args()


def function_arg(arg):
    try:
        return int(arg)
    except ValueError:
        try:
            return float(arg)
        except ValueError:
            return arg


def main():
    args = parse_args()
    if args.test:
        run_tests()
    elif args.debug:
        mod_name = Path(args.debug).stem
        mod_spec = importlib.util.spec_from_file_location(mod_name, args.debug)
        module = importlib.util.module_from_spec(mod_spec)
        mod_spec.loader.exec_module(module)
        func = getattr(module, args.function[0])

        output_path = args.output
        this_args = [function_arg(arg) for arg in args.function[1:]]

        debugger = PyBud()
        debugger.run_debug(output_path, func, this_args)

        if args.video:  # user wants a video render
            vlogger = VideoLogger(output_path)

        else:  # if not, print the log in human readable form to console
            logger = ConsoleLogger(output_path)
            logger.print_log()
    elif args.parse:
        file_path = args.parse

        if args.video:  # user wants a video render
            vlogger = VideoLogger(file_path)

        else:  # if not, print the log in human readable form to console
            logger = ConsoleLogger(file_path)
            logger.print_log()
    else:  # no args, just run test on example
        output_path = "example.pybud"

        debugger = PyBud()
        debugger.run_debug(output_path, sample, (3, 2))

        logger = ConsoleLogger(output_path)
        logger.print_log()


if __name__ == '__main__':
    main()
