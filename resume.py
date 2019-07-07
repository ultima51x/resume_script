import argparse
import os
from datetime import date
from subprocess import call

import settings
from node import tree_from_filename
from printers import HtmlPrinter, TexPrinter, TextPrinter


class ResumeParser:
    def __init__(self, printer):
        self.printer = printer
        pass

    def read_from(self, filename, longmode):
        return self.printer.render(tree_from_filename(filename, longmode))


def main():
    parser = argparse.ArgumentParser(
        description='Output a resume to different formats.')
    parser.add_argument('-l',
                        '--long',
                        dest='longmode',
                        action='store_true',
                        default=False,
                        help='sum the integers (default: find the max)')
    args = parser.parse_args()

    longmode = args.longmode

    basename = os.path.join(
        settings.TARGET_DIR, "{0}{1}".format(settings.RESUME_NAME,
                                             date.today().isoformat()))
    source = settings.XML_SOURCE

    text = "{0}.txt".format(basename)
    with open(text, 'w') as f:
        output = ResumeParser(TextPrinter()).read_from(source, longmode)
        f.write(output)

    html = "{0}.html".format(basename)
    with open(html, 'w') as f:
        output = ResumeParser(HtmlPrinter()).read_from(source, longmode)
        f.write(output)

    latex = "{0}.tex".format(basename)
    with open(latex, 'w') as f:
        output = ResumeParser(TexPrinter()).read_from(source, longmode)
        f.write(output)
    call(["pdflatex", "-output-directory", settings.TARGET_DIR, latex])

    print("Outputted to {0}".format(settings.TARGET_DIR))


if __name__ == "__main__":
    main()
