import argparse
import os
from datetime import date
from subprocess import call

from node import tree_from_filename
from printers import HtmlPrinter, TexPrinter, TextPrinter


class ResumeParser:
    def __init__(self, printer):
        self.printer = printer
        pass

    def read_from(self, filename, longmode):
        return self.printer.render(tree_from_filename(filename, longmode))


def prog():
    defaults = {
        "outdir": "./outdir",
        "fnameprefix": "resume_",
    }

    parser = argparse.ArgumentParser(
        description="Output resume data (in xml format) to different formats."
    )
    parser.add_argument(
        "source",
        action="store",
        metavar="SOURCEXML",
        help="source xml file of resume data",
    )
    parser.add_argument(
        "-l",
        "--long",
        dest="longmode",
        action="store_true",
        default=False,
        help="sum the integers (default: find the max)",
    )
    parser.add_argument(
        "--out",
        dest="target_dir",
        action="store",
        metavar="OUTDIR",
        default=defaults["outdir"],
        help="directory to output to (default: {0})".format(defaults["outdir"]),
    )
    parser.add_argument(
        "--fnameprefix",
        dest="fnameprefix",
        action="store",
        metavar="PREFIX",
        default=defaults["fnameprefix"],
        help="start of the filename of the files (default: {0})".format(
            defaults["fnameprefix"]
        ),
    )

    return parser


def main():
    args = prog().parse_args()

    source = args.source
    longmode = args.longmode
    targetdir = args.target_dir
    fnameprefix = args.fnameprefix
    if not os.path.exists(targetdir):
        os.makedirs(targetdir)

    basename = os.path.join(
        targetdir, "{0}{1}".format(fnameprefix, date.today().isoformat())
    )

    text = "{0}.txt".format(basename)
    with open(text, "w") as f:
        output = ResumeParser(TextPrinter()).read_from(source, longmode)
        f.write(output)

    html = "{0}.html".format(basename)
    with open(html, "w") as f:
        output = ResumeParser(HtmlPrinter()).read_from(source, longmode)
        f.write(output)

    latex = "{0}.tex".format(basename)
    with open(latex, "w") as f:
        output = ResumeParser(TexPrinter()).read_from(source, longmode)
        f.write(output)
    call(["pdflatex", "-output-directory", targetdir, latex])

    print("Outputted to {0}".format(targetdir))


if __name__ == "__main__":
    main()
