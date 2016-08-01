import graphics


def load(d, path):
    if hasattr(d, "tag") and d.tag == "img" and "src" in d.attr:
        d.img = graphics.img_load(path + d.attr["src"])
    for c in d.children:
        load(c, path)
