from typing import Dict, List
from xml.etree.ElementTree import Element, parse


def tree_from_filename(fname: str, longmode: bool):
    Node.long_mode = longmode
    tree = parse(fname)
    return Node(tree.getroot())


def xmlelem_to_node(elem: Element):
    t = elem.tag
    n: Node

    if t == 'header':
        n = Header(elem)
    elif t == 'sec':
        n = Section(elem)
    elif t == 'pos':
        n = Position(elem)
    elif t == 'desc':
        n = Description(elem)
    elif t == 'loc':
        n = Location(elem)
    elif t == 'list':
        n = EntryList(elem)
    elif t == 'entry':
        n = Entry(elem)
    elif t == 'body':
        n = Node(elem)
    else:
        n = Node(elem)

    return n


class Node:
    long_mode: bool = False

    def __init__(self, node: Element):
        self.tag = node.tag
        self._attrs: Dict[str, str] = node.attrib
        self.text: str = node.text or ''
        self._levelstr: str = self.get('level')
        self._children: List[Element] = node.getchildren()

    def in_long(self) -> bool:
        return "long" in self._levelstr

    def in_short(self) -> bool:
        return "short" in self._levelstr

    def get(self, key: str) -> str:
        return self._attrs.get(key, '')

    def shown(self) -> bool:
        if self.long_mode:
            return self.in_long()
        else:
            return self.in_short()

    def children(self) -> List['Node']:
        parsed = [xmlelem_to_node(c) for c in self._children]
        return [c for c in parsed if c.shown()]


class Header(Node):
    def __init__(self, node):
        super().__init__(node)
        self.name = self.get('name')
        self.address1 = self.get('address1')
        self.address2 = self.get('address2')
        self.phone = self.get('phone')
        self.email = self.get('email')


class Section(Node):
    def __init__(self, node):
        super().__init__(node)
        self.name = self.get('name')


class Location(Node):
    def __init__(self, node):
        super().__init__(node)
        self.name = self.get('value')
        self.city = self.get('city')


class Position(Node):
    def __init__(self, node):
        super().__init__(node)
        self.name = self.get('value')
        self.date = self.get('date')
        self.description = self.get('description')


class Description(Node):
    def __init__(self, node):
        super().__init__(node)


class EntryList(Node):
    def __init__(self, node):
        super().__init__(node)
        self.title = self.get('title')


class Entry(Node):
    def __init__(self, node):
        super().__init__(node)
