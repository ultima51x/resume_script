# resume script

This is a python script which is able to read the contents of a resume in an XML format and then print out a text file, HTML, and PDF (via latex and pdflatex).

A sample resume file is included in `resume_example.xml`.

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
