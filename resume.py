import os
import sys
from datetime import date
from subprocess import call

import settings
from node import tree_from_filename
from printers import HtmlPrinter, TexPrinter, TextPrinter


class ResumeParser:
    def __init__(self, printer):
        self.printer = printer
        pass

    def render(self, filename):
        return self.printer.render(tree_from_filename(filename))


def main():
    basename = os.path.join(
        settings.TARGET_DIR, "{0}{1}".format(settings.RESUME_NAME,
                                             date.today().isoformat()))

    text = "{0}.txt".format(basename)
    html = "{0}.html".format(basename)
    latex = "{0}.tex".format(basename)
    # debug = "{0}.debug.txt".format(basename)

    sys.stdout = open(text, 'w')
    output = ResumeParser(TextPrinter()).render(settings.XML_SOURCE)
    print(output)

    sys.stdout = open(html, 'w')
    output = ResumeParser(HtmlPrinter()).render(settings.XML_SOURCE)
    print(output)

    sys.stdout = open(latex, 'w')
    output = ResumeParser(TexPrinter()).render(settings.XML_SOURCE)
    print(output)

    sys.stdout = sys.__stdout__
    # call(["pdflatex", "-output-directory", settings.TARGET_DIR, latex])

    print("Output to {0}".format(settings.TARGET_DIR))
    print("OK")


if __name__ == "__main__":
    main()
