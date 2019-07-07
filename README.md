# resume script

This is a python script which is able to read the contents of a resume in an XML format and then print out a text file, HTML, and PDF (via latex and pdflatex).

## Creating a XML file

A sample resume file is included in `resume_example.xml`.

A primary feature is the idea of levels. I've had trouble with limiting a resume to 1 page, so I've built in functionality which lets one specify which XML elements get processed.  XML elements with level short will print in short mode, long in long mode.  Long mode can be enabled with flag `-l` or `--long`.  Otherwise, short mode is used.


## Requirements
* Python 3.7
* `latex` and `pdflatex`
* The resume latex class located http://www.ctan.org/tex-archive/macros/latex/contrib/resume/res.cls

## Installation

* Create a new virtual env
```
python -m venv env
source env/bin/activate
```
* Install deps from requirements.txt: `pip install -r requirements.txt`


## Instructions
To run this within the virtual environment, `python resume.py resume_example.xml`.
Run `python resume.py -h` for more help.
