class TexPrinter:
    def __init__(self):
        pass

    def before(self,elem):
        name = elem.tag
        attrs = elem.attrib
        data = elem.text

        if name == "root":
            print """% LaTeX file for resume
% This file uses the resume document class (res.cls)

\documentclass[margin]{res}
%\usepackage{helvetica} % uses helvetica postscript font (download helvetica.sty)
%\usepackage{newcent}   % uses new century schoolbook postscript font
%\\newsectionwidth{0pt}  % So the text is not indented under section headings
%\\usepackage{fancyhdr}  % use this package to get a 2 line header
%\\renewcommand{\headrulewidth}{0pt} % suppress line drawn by default by fancyhdr
%\setlength{\headheight}{24pt} % allow room for 2-line header
%\setlength{\headsep}{24pt}  % space between header and text
%\setlength{\headheight}{24pt} % allow room for 2-line header
%\pagestyle{fancy}     % set pagestyle for document
%\\rhead{ {\it D. Hwang}\\\\{\it p. \\thepage} } % put text in header (right side)
%\\cfoot{}                                     % the foot is empty
\\topmargin=-0.75in % start text higher on the page
\oddsidemargin=-0.65in
\evensidemargin=-0.65in
\\addtolength{\\textwidth}{1.25in}
\\addtolength{\\textheight}{1.25in}

\\begin{document}
\\thispagestyle{empty} % this page has no header"""
        elif name == "name": print "\\address{\\bf\\LARGE",
        elif name == "phone": print "\\address{",
        elif name == "sec":
            print "\\section{" + attrs["name"].upper() + "}"
            if attrs["desc"] == "": pass
            else: print attrs["desc"]
        elif name == "loc":
            print "{\\bf", attrs["value"], "}\\hfill", attrs["city"] + "\\\\"
        elif name == "pos":
            print "{\\it", attrs["value"], "}\\hfill", attrs["date"]
            print "\\begin{itemize} \\itemsep -2pt"
        elif name == "desc":
            if attrs["type"] == "inner":
                print "\item[$\circ$]",
            else:
                print "\item",
        elif name == "space":
            print "\\vspace {+10pt}"

        if data is None or data[0] == '\n' or data[0] == "\t" or data[0] == ' ': pass
        else: print data,

    def after(self,elem):
        name = elem.tag

        if name in ("name","address1","phone","email"): print "\\\\",
        elif name in ("address2","website"):
            print "}"
            if name == "website": print "\n\n\\begin{resume}"
        elif name == "pos": print "\\end{itemize}\n\\vspace {-10pt}"
        elif name == "root": print """\\end{resume}
\\end{document}"""
        elif name == "desc": print

class TextPrinter:
    def before(self, elem):
        name = elem.tag
        attrs = elem.attrib
        data = elem.text

        if name == "sec":
            print "----------------------------------"
            print attrs["name"].upper()
            print "----------------------------------"
            print
            if attrs["desc"] == "": pass
            else: print attrs["desc"]
        elif name == "loc":
            print attrs["value"].upper()
            print attrs["city"]
            print
        elif name == "pos":
            print attrs["value"]
            print "(" + attrs["date"] + ")",
            print
        elif name == "desc": print "*",

        if data is None or data[0] == '\n' or data[0] == "\t" or data[0] == ' ': pass
        else: print data

    def after(self,elem):
        #extra line after these sections are over
        if elem.tag in ("sec","pos","name","phone","website"): print


class HtmlPrinter:
    def before(self, elem):
        name = elem.tag
        attrs = elem.attrib
        data = elem.text

        if name == "name": print "<h1>",
        elif name == "sec":
            print "<h2>" + attrs["name"] + "</h2>"
            if attrs["desc"] == "": pass
            else: print "<p>" + attrs["desc"] + "</p>"
        elif name == "loc":
            print "<h3>" + attrs["value"], "-", attrs["city"] + "</h3>"
        elif name == "pos":
            print "<h4>" + attrs["value"], "(" + attrs["date"] + ")" "</h4>"
            print "<ul>"
        elif name == "desc": print "<li>",

        if data is None or data[0] == '\n' or data[0] == "\t" or data[0] == ' ': pass
        else: print data,

    def after(self, elem):
        name = elem.tag

        if name == "name": print "</h1>"
        elif name == "website": print "</p>"
        elif name in ("address1","address2","website","phone","email"):
            print "<br/>"
            if name in ("phone"): print "<br/>"
        elif name == "pos": print "</ul>"
        elif name == "desc": print "</li>"

class DebugPrinter:
    def before(self, elem):
        print "before", elem.tag, elem.attrib, elem.text

    def after(self, elem):
        print "after", elem.tag, elem.attrib, elem.text
