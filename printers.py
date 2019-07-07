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
