import re


class DOMNode:
    """DOM Node Class"""
    def __init__(self):
        self.children = []
        self.type = ""


def __escape_scape(s, p):
    while p < len(s):
        if s[p].isspace():
            p += 1
        else:
            break
    return p


def __format_attr(s):
    t = ""
    s = s.replace("'",'"')
    for p in range(0, len(s)):
        if not s[p].isspace():
            t += s[p]
    return t


# dose not support attr like "with=100" yet
def __parse_attr(attr_str):
    attr_str = __format_attr(attr_str).replace("=", '')
    arr = attr_str.split('"')
    del(arr[-1])
    attr = {arr[x]: arr[x + 1] for x in range(0, len(arr), 2)}
    return attr


def __parse_children(node, html_lines, pos):
    while pos < len(html_lines):
        pos = __escape_scape(html_lines, pos)
        if html_lines[pos] is '<':
            pos += 1  # pass '<'
            if html_lines[pos] is '/':
                # close tag parse over
                while html_lines[pos] is not '>':
                    pos += 1
                return pos + 1  # pass '>'
            # start of a tag
            else:
                tag_strt = pos
                child = DOMNode()
                child.attr = {}
                attr_end = pos
                while html_lines[pos] is not '>':
                    if html_lines[pos].isspace():
                        # attr
                        while html_lines[attr_end] is not '>':
                            attr_end += 1
                        child.attr = __parse_attr(html_lines[pos:attr_end])
                        break
                    pos += 1

                child.type = "ELEM"
                child.tag = html_lines[tag_strt:pos]
                child.parent = node
                node.children.append(child)

                while html_lines[pos] != '>':
                    pos += 1

                pos += 1  # pass '>'

                pos = __parse_children(child, html_lines, pos)
        else:
            # text node

            start = pos

            while pos < len(html_lines) and html_lines[pos] is not '<':
                pos += 1

            child = DOMNode()
            child.type = "TEXT"
            child.content = html_lines[start:pos]
            child.parent = node
            node.children.append(child)


def parse(html):
    # replace self-closing tag like <img /> to <img></ >
    html = html.replace("/>", "></ >")
    # remove comments
    html = re.sub("<!--.*-->", "", html, flags=re.MULTILINE)
    root = DOMNode()
    root.type = "ROOT"
    __parse_children(root, html, 0)
    root.parent = None
    return root



