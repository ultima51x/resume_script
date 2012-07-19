#David Hwang
#Takes in XML file, then outputs a .txt, .html (body only), and a LATEX file

import sys
import xml.parsers.expat

# handler functions for text
def txt_start_element(name, attrs):
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

def txt_end_element(name):
    #extra line after these sections are over
    if name in ("sec","pos","name","phone","website"): print

def txt_char_data(data):
    if data[0] == '\n' or data[0] == "\t" or data[0] == ' ': pass
    else: print data
    
# Handler functions for html
def html_start_element(name, attrs):
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

def html_end_element(name):
    if name == "name": print "</h1>"
    elif name == "website": print "</p>"
    elif name in ("address1","address2","website","phone","email"):
        print "<br/>"
        if name in ("phone"): print "<br/>"
    elif name == "pos": print "</ul>"
    elif name == "desc": print "</li>"

def html_char_data(data):
    if data[0] == '\n' or data[0] == "\t" or data[0] == ' ': pass
    else: print data,

# Handler functions for tex
def tex_start_element(name, attrs):
    #header
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
    
def tex_end_element(name):
    if name in ("name","address1","phone","email"): print "\\\\",
    elif name in ("address2","website"):
        print "}"
        if name == "website": print "\n\n\\begin{resume}"
    elif name == "pos": print "\\end{itemize}\n\\vspace {-10pt}"
    elif name == "root": print """\\end{resume}
\\end{document}"""
    elif name == "desc": print

def tex_char_data(data):
    if data[0] == '\n' or data[0] == "\t" or data[0] == ' ': pass
    else: print data,

# Handler functions for debugging
def start_element(name, attrs):
    print 'Start element:', name, attrs
def end_element(name):
    print 'End element:', name
def char_data(data):
    print 'Character data:', repr(data)

# Main function for setting up parser handlers and input/output
def main():    
    sys.stdout = open("../david_hwang_resume.txt",'w')    
    p1 = xml.parsers.expat.ParserCreate()
    p1.StartElementHandler = txt_start_element
    p1.EndElementHandler = txt_end_element
    p1.CharacterDataHandler = txt_char_data
    p1.Parse(open("./david_hwang_resume.xml",'r').read())

    sys.stdout = open("../david_hwang_resume.html",'w')    
    p2 = xml.parsers.expat.ParserCreate()
    p2.StartElementHandler = html_start_element
    p2.EndElementHandler = html_end_element
    p2.CharacterDataHandler = html_char_data
    p2.Parse(open("./david_hwang_resume.xml",'r').read())

    sys.stdout = open("../david_hwang_resume.tex",'w')    
    p3 = xml.parsers.expat.ParserCreate()
    p3.StartElementHandler = tex_start_element
    p3.EndElementHandler = tex_end_element
    p3.CharacterDataHandler = tex_char_data
    p3.Parse(open("./david_hwang_resume.xml",'r').read())

    sys.stdout = open("../debug_output",'w')    
    p4 = xml.parsers.expat.ParserCreate()
    p4.StartElementHandler = start_element
    p4.EndElementHandler = end_element
    p4.CharacterDataHandler = char_data
    p4.Parse(open("./david_hwang_resume.xml",'r').read())
    
if __name__ == "__main__":
    main()    
        
