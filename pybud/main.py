#!/usr/bin/env python3
import argparse
import importlib
import os
from pathlib import Path

from pybud.ConsoleLogger import ConsoleLogger
from pybud.PyBud import PyBud
from pybud.video.VideoLogger import VideoLogger
from pybud.example import sample
from pybud.tests.perform_tests import run_tests


def parse_args():
    parser = argparse.ArgumentParser(
        description="A Python debugger for analyzing and profiling functions. Created by Eastan Giebler."
    )

    parser.add_argument(
        "-t",
        "--test",
        action="store_true",
        help="Test PyBud on a suite of sorting, searching, and similar algorithms. "
             "Outputs a PyBud JSON for each function in the 'pybud/test/test_logs' package. "
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
        "-o",
        "--output",
        default="output.pybud",
        metavar="FILE",
        help="Optional: Path to write the json log file to. Defaults to output.pybud if argument not used."
    )

    video = debugging.add_argument(
        "-v",
        "--video",
        nargs='?',
        const="output.mp4",
        metavar="FILE",
        help="Generate a video rendering for the PyBud debug steps of the program flow. "
             "Optional: provide a filepath to output to, defaults to output.mp4. "
    )

    parsing = parser.add_argument_group(title="Parsing and Analysis",
                                        description="Parse a PyBud JSON output and display in human-readable form.")
    parsing.add_argument(
        "-p",
        "--parse",
        nargs='?',
        const="output.pybud",
        metavar="FILE",
        help="Path to the json log you wish to parse into human-readable form. "
             "Defaults to output.pybud if a file is not specified."
    )

    parsing._group_actions.append(video)  # make video option also available to parser

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

    os.system('')  # allows for colors to be printed in console
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
            vlogger.generate(args.video)
        else:  # if not, print the log in human readable form to console
            logger = ConsoleLogger(output_path)
            logger.print_log()
    elif args.parse:
        file_path = args.parse

        if args.video:  # user wants a video render
            vlogger = VideoLogger(file_path)
            vlogger.generate(args.video)
        else:  # if not, print the log in human readable form to console
            logger = ConsoleLogger(file_path)
            logger.print_log()
    else:  # no args, just run test on example
        test_dir = Path(__file__).parent / "debug"
        Path(str(test_dir)).mkdir(parents=True, exist_ok=True)

        output_path = str(test_dir / "example.pybud")

        debugger = PyBud()
        debugger.run_debug(output_path, sample, (3, 2))

        logger = ConsoleLogger(output_path)
        logger.print_log()

        vlogger = VideoLogger(output_path)
        vlogger.generate(str(test_dir / "test.mp4"))


if __name__ == '__main__':
    main()
