# PyBud

PyBud is a Python debugging and profiling tool that generates videos of step-by-step code execution.

Here's a PyBud example output from debugging a bubble sort algorithm!

https://streamable.com/s/9ubtq/kudngz

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install PyBud.

```bash
pip install pybud
```

## Usage Example

![Usage](recordings/demo.gif)

## Usage

Once installed, running `pybud --help` will give you an overview of how to use PyBud.

Here's the help output:

```bash
$ pybud -h
usage: pybud [-h] [-t] [-d FILE] [-f FUNCTION [FUNCTION ...]] [-o FILE] [-v [FILE]] [-c CONFIG] [-p [FILE]]

A Python debugger for analyzing and profiling functions. Created by Eastan Giebler.

optional arguments:
  -h, --help            show this help message and exit
  -t, --test            Test PyBud on a suite of sorting, searching, and similar algorithms. Outputs a PyBud JSON for each function in the
                        'pybud/test/test_logs' package.

Debugging:
  Debug a python function and generate an output log.

  -d FILE, --debug FILE
                        Path to the Python file you wish to debug.
  -f FUNCTION [FUNCTION ...], --function FUNCTION [FUNCTION ...]
                        The function in the Python file you wish to debug, along with the arguments you wish to pass. Defaults to the main
                        function if argument not used. EXAMPLE: '--function test 2 4' will call 'test(2,4)'.
  -o FILE, --output FILE
                        Optional: Path to write the json log file to. Defaults to output.pybud if argument not used.
  -v [FILE], --video [FILE]
                        Generate a video rendering for the PyBud debug steps of the program flow. Optional: provide a filepath to output to,
                        mp4 is the only supported format, defaults to output.mp4.
  -c CONFIG, --video-cfg CONFIG
                        Path to the YAML video config file you wish to use, default configuration will be loaded if not specified.

Parsing and Analysis:
  Parse a PyBud JSON output and display in human-readable form.

  -p [FILE], --parse [FILE]
                        Path to the json log you wish to parse into human-readable form. Defaults to output.pybud if a file is not specified.
  -v [FILE], --video [FILE]
                        Generate a video rendering for the PyBud debug steps of the program flow. Optional: provide a filepath to output to,
                        mp4 is the only supported format, defaults to output.mp4.
  -c CONFIG, --video-cfg CONFIG
                        Path to the YAML video config file you wish to use, default configuration will be loaded if not specified.
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
