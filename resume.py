import sys
import xml.etree.ElementTree as ET
from datetime import date
from subprocess import call

from printers import TexPrinter
from printers import TextPrinter
from printers import HtmlPrinter
from printers import DebugPrinter

class ResumeParser:
    def __init__(self,printer):
        self.printer = printer
        pass

    def read(self,filename):
        tree = ET.parse(filename)
        self.process(tree.getroot())

    def process(self,elem):
        if "skip" in elem.attrib:
            return

        self.printer.before(elem)

        for child in elem:
            self.process(child)

        self.printer.after(elem)

def main():
    input_file = "./david_hwang_resume.xml"
    basename = "david_hwang_resume_{0}".format(date.today().isoformat())

    text = "./output/{0}.txt".format(basename)
    html = "./output/{0}.html".format(basename)
    latex = "./output/{0}.tex".format(basename)
    debug = "./output/{0}.debug.txt".format(basename)

    sys.stdout = open(text,'w')
    ResumeParser(TextPrinter()).read(input_file)

    sys.stdout = open(html,'w')
    ResumeParser(HtmlPrinter()).read(input_file)

    sys.stdout = open(latex,'w')
    ResumeParser(TexPrinter()).read(input_file)

    sys.stdout = open(debug,'w')
    ResumeParser(DebugPrinter()).read(input_file)

if __name__ == "__main__":
    main()

