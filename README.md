# Python Algorithm Task Generator

This python program generates tasks written in LaTeX (in englisch and german) for various algorithms. Most algorithms are based upon Cormen, Leiserson, Rivest, Stein. Introduction to Algorithms 4ed. 2022. MIT Press. Its aim is to provide students learning these algorithms a way to execute them on different inputs and to ease the work on creating such exercises for educators, as it is often required for undergraduate algorithm courses.

## Requirements
- [python 3.8+](https://www.python.org)
- [pyaml](https://pypi.org/project/pyaml/) (for reading localisation files)
- [pylatex](https://pypi.org/project/PyLaTeX/) (for generating LaTeX code)
- [latexmk](https://ctan.org/pkg/latexmk) (for compiling LaTeX code)

## How to Run
Download the latest release, extract the files and execute python on the folder, e.g.

    python3 pyAlgoTask TASK_CATEGORY TASK [optional Arguments]

Please not that you need to give at least the task category, the task and a file location for the exercise or for the solutuion for the program to do anything.

Alternatively you can locally install the program using

    pip install ./pyAlgoTask

and using

    pyAlgoTask TASK_CATEGORY TASK [optional Arguments]

in the commandline.

## How to Use
We specify ever task in a category. We currently support the following categories and tasks:

- Sorting
  - Bubblesort
  - Bucketsort (on numbers between 0 and 1)
  - Countingsort
  - Heapsort
  - Insertionsort
  - Mergesort
  - Quicksort with Lomutos partition scheme
  - Quicksort with Hoares partition scheme
  - Radixsort (on non-negative numbers)
  - Selectionsort

- Hashing
  - Closed Hashing using double hashing
  - Closed Hashing using linear probing
  - Closed Hashing using quadratic probing
  - Open Hashing
  
  with the hash functions:
  - Divison method (modulo table size)
  - Multiplication method (scaling to table size)
  - Bit-shift method

All tasks currently support only LaTeX output. You need to provide a file to write the source code into using parameters `-e` for exercise and `-s` for solution. Additionally you may use `--pdf` and `--view` to generate a pdf and directly view the pdf in a viewer respectively.

Generally, for input the parameters `-i` are used for commandline input and `-f` for file input. The syntax of the input is explained in the help files for each task. If no input is given, a random input is generated with certain heuristical bounds.

Further customization is possible and explained in the help for each task.

### Virtual Environment
You may need to use a virtual environment to install pylatex. To do this, execute the following

    python -m venv ./venv
    source ./venv/bin/activate

## Project Structure
This project is structured in five parts, the [Main part](#main-part), the [Tasks](#tasks), the [Input modules](#input), the [Randomizer modules](#randomizer) and the [Output modules](#output). Additionally, we use unittesting with [pytest](https://pytest.org/).

### Main part
The main class `src/pyAlgoTask/__man__` deals with reading the parser and calling all other modules. This includes error handling, to call the exporter `src/pyAlgoTask/export` for file export and allowing all tasks to register themself using the module `src/pyAlgoTask/tasks/tasks.py` and their argument parsers. Most modules have the possibility to register parser options themself (using [argparse](https://docs.python.org/3/library/argparse.html)) and to parse the parameter themself.

### Tasks
The folder `src/pyAlgoTask/tasks` contain one folder for each category, containing one file per task classes. Tasks classes handle the algorithm to generate a task for and the various modules surrounding this task. Theses are especially [Input Modules](#Input), [Randomizer Modules](#Randomizer), the language pick module `src/pyAlgoTask/language.py` and various data structures or wrapper classes from `src/pyAlgoTask/structures.py`.

#### Algorithm Method
The algorithm is implemented as a generator `def algorithm(self): ... `, that yields intermediate steps are required by the task. Usually, the generator yields a tuple, where the first entry is the actual output and the second are highlighting information, if used. The generator is called by the [Output Module](#Output) when the exercise and solution code is generated.

### Input
This module has various classes for handling various input types, e.g. arrays for sorting or insert/delete operations for data structures. They are generally assumes to register arguments to [argparse](https://docs.python.org/3/library/argparse.html) and to read them from argparse.

### Randomizer
Generally, every Input module also has a Randomizer module to generate a certain random input for in case no input was given. This design follows the parser-randomizer dualism.

### Output
Output modules are used to generate LaTeX code for certain types of tasks. Since tasks are rather diverse, so are their respective output modules. Generally speaking, the exercise file contains first some text, usually consisting of a pretext, the input for the algorithm, followed by a posttext. Lastly space for entering the solution is given. The space is roughly oriented on the solution, but sometimes a bit more space is given (i.e. for open hashing we offer sufficient place to insert every item at one position)

### Testing
The module `tests/...` offer various testing classes using [pytest](https://pytest.org/) with [mock](https://docs.python.org/3/library/unittest.mock.html) and [pytest-timeout](https://pypi.org/project/pytest-timeout/). We use one testing file per category, where we try to test all algorithms in the same class similarly or even the same to enforce uniformity.

### Documentation
Documentation is designed for pydoctor using the command

    pydoctor --make-html --html-output=docs/api --docformat=restructuredtext src/pyalgotask

in the root directory

## How to Contribute
Please open an issue if you found bugs or have feature requests. The feature requests may be added to the TODO file in this repository.

If you would like to contribute code, please use the following tools:

* pylint
* black formatter
* pydoctor
* pytest

And open an pull request detailing your contribution.

## Credits
This tool is developed by:
* Ira Fesefedt

## License
The MIT License (MIT)

Copyright (c) 2023 Ira Fesefeldt

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.