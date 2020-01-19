# PyBud

PyBud is a Python tool for debugging and profiling python functions.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install PyBud.

```bash
pip install pybud
```

## Demo

![Demo](recordings\demo.gif)

## Usage

Once installed, running `pybud --help` will give you an overview of how to use PyBud.

Here's the help output:

```bash
$ pybud --help
usage: pybud [-h] [-d FILE] [-f FUNCTION [FUNCTION ...]] [-v] [-o FILE] [-p [FILE]] [-t]

A Python debugger for analyzing and profiling functions. Created by Eastan Giebler.

optional arguments:
  -h, --help            show this help message and exit

Debugging:
  Debug a python function and generate an output log.

  -d FILE, --debug FILE
                        Path to the Python file you wish to debug.
  -f FUNCTION [FUNCTION ...], --function FUNCTION [FUNCTION ...]
                        The function in the Python file you wish to debug, along with the arguments you wish to pass.
                        Defaults to the main function if argument not used. EXAMPLE: '--function test 2 4' will call
                        'test(2,4)'.
  -v, --video           Generate a video rendering for the PyBud debug steps of the program flow.
  -o FILE, --output FILE
                        Optional: Path to write the json log file. Defaults to output.pybud if argument not used.

Parsing and Analysis:
  Parse a PyBud JSON output and display to console in human-readable form.

  -p [FILE], --parse [FILE]
                        Path to the json log you wish to parse into human-readable form. Defaults to output.pybud if a
                        file is not specified.
  -t, --test            Test PyBud on a suite of sorting, searching, and similar algorithms. Outputs a PyBud JSON for
                        each function in the 'test/test_logs' package.
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)