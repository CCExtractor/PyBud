#!/usr/bin/env python3
import argparse
import importlib
from pathlib import Path

from pybud.ConsoleLogger import ConsoleLogger
from pybud.PyBud import PyBud


def parse_args():
    parser = argparse.ArgumentParser(
        description="A Python debugger for analyzing and reporting functions. Created by Eastan Giebler."
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
        help="Optional: the function in the Python file you wish to debug, along with the arguments you wish to pass."
             "Defaults to the main function if not provided. "
             "EXAMPLE: '--function test 2 4' will call 'test(2,4)'."
    )

    debugging.add_argument(
        "-o",
        "--output",
        default="output.pybud",
        metavar="FILE",
        help="Optional: Path to write the json log file. Defaults to output.pybud"
    )

    parsing = parser.add_argument_group(title="Parsing",
                              description="Parse a PyBud JSON output and display to console in human-readable form.")
    parsing.add_argument(
        "-p",
        "--parse",
        default="output.pybud",
        metavar="FILE",
        help="Path to the json log you wish to parse into human-readable form. Defaults to output.pybud"
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

    if args.debug:
        mod_name = Path(args.debug).stem
        mod_spec = importlib.util.spec_from_file_location(mod_name, args.debug)
        module = importlib.util.module_from_spec(mod_spec)
        mod_spec.loader.exec_module(module)

        output_path = args.output
        this_args = [function_arg(arg) for arg in args.function[1:]]

        debugger = PyBud()
        debugger.run_debug(output_path, module, args.function[0], this_args)

        logger = ConsoleLogger(output_path)
        logger.print_log()
    elif args.parse:
        file_path = args.parse
        logger = ConsoleLogger(file_path)
        logger.print_log()


if __name__ == '__main__':
    main()
