from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader, contextfilter


@contextfilter
def call_macro_by_name(context, macro_name, *args, **kwargs):
    return context.vars[macro_name](*args, **kwargs)


class TexPrinter:
    def render(self, node):
        env = Environment(loader=FileSystemLoader('templates'),
                          block_start_string='\BLOCK{',
                          block_end_string='}',
                          variable_start_string='\VAR{',
                          variable_end_string='}',
                          comment_start_string='\#{',
                          comment_end_string='}',
                          line_statement_prefix='%%',
                          line_comment_prefix='%#',
                          trim_blocks=True,
                          lstrip_blocks=True,
                          autoescape=False)
        env.filters['macrobyname'] = call_macro_by_name
        template = env.get_template('base.tex')
        return template.render(node=node)

    def before(self, elem):
        name = elem.tag
        attrs = elem.attrib
        data = elem.text

        if name == "root":
            print("""% LaTeX file for resume
% This file uses the resume document class (res.cls)

\documentclass[margin]{res}
%\\usepackage{helvetica} % uses helvetica postscript font (download helvetica.sty)
%\\usepackage{newcent}   % uses new century schoolbook postscript font
%\\newsectionwidth{0pt}  % So the text is not indented under section headings
%\\usepackage{fancyhdr}  % use this package to get a 2 line header
%\\renewcommand{\headrulewidth}{0pt} % suppress line drawn by default by fancyhdr
%\setlength{\headheight}{24pt} % allow room for 2-line header
%\setlength{\headsep}{24pt}  % space between header and text
%\setlength{\headheight}{24pt} % allow room for 2-line header
%\pagestyle{fancy}     % set pagestyle for document
%\\rhead{ {\it D. Hwang}\\\\{\it p. \\thepage} } % put text in header (right side)
%\\cfoot{}                                     % the foot is empty
\\topmargin=-0.85in % start text higher on the page
\oddsidemargin=-0.65in
\evensidemargin=-0.65in
\\addtolength{\\textwidth}{1.25in}
\\addtolength{\\textheight}{1.55in}

\\begin{document}
\\thispagestyle{empty} % this page has no header""")
        elif name == "name":
            print("\\address{\\bf\\LARGE", end=' ')
        elif name == "phone":
            print("\\address{", end=' ')
        elif name == "sec":
            print("\\section{" + attrs["name"].upper() + "}")
            if attrs["desc"] == "": pass
            else: print(attrs["desc"])
        elif name == "loc":
            print("{\\bf", attrs["value"], "}\\hfill", attrs["city"] + "\\\\")
        elif name == "pos":
            print("{\\it", attrs["value"], "}\\hfill", attrs["date"])
            print("\\begin{itemize} \\itemsep -2pt")
        elif name == "desc":
            if attrs["type"] == "inner":
                print("\item[$\circ$]", end=' ')
            else:
                print("\item", end=' ')
        elif name == "text":
            print("{\\bf", attrs["header"] + ":} ", end=' ')
        elif name == "space":
            print("\\vspace {+10pt}")
        elif name == "br":
            print("\\\\")

        if data is None or data[0] == '\n' or data[0] == "\t" or data[0] == ' ':
            pass
        else:
            print(data, end=' ')

    def after(self, elem):
        name = elem.tag

        if name in ("name", "address1", "phone", "email"):
            print("\\\\", end=' ')
        elif name in ("address2", "website"):
            print("}")
            if name == "website": print("\n\n\\begin{resume}")
        elif name == "pos": print("\\end{itemize}\n\\vspace {-10pt}")
        elif name == "root": print("""\\end{resume}
\\end{document}""")
        elif name == "desc": print()


class TextPrinter:
    def render(self, node):
        env = Environment(loader=FileSystemLoader('templates'),
                          lstrip_blocks=True,
                          trim_blocks=True)
        env.filters['macrobyname'] = call_macro_by_name
        template = env.get_template('base.txt')
        return template.render(node=node)


class HtmlPrinter:
    def render(self, node):
        env = Environment(loader=FileSystemLoader('templates'),
                          lstrip_blocks=True,
                          trim_blocks=True)
        env.filters['macrobyname'] = call_macro_by_name
        template = env.get_template('base.html')
        markup_string = template.render(node=node)
        soup = BeautifulSoup(markup_string, 'html.parser')
        return soup.prettify()
