# resume script

This is a python script which is able to read the contents of a resume in an XML format and then print out a text file, HTML, and PDF (via latex and pdflatex).

## Requirements
* Python 2
* latex and pdflatex
* The resume latex class located http://www.ctan.org/tex-archive/macros/latex/contrib/resume/res.cls

Three configuration variables must be set in settings.py.  You can make a copy from settings.py.example
* `TARGET_DIR` is where the result files will be output.  It should already exist.
* `XML_SOURCE` is the location of the xml file with the resume.
* `RESUME_NAME` is the name of the resulting files.
