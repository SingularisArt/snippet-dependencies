import re


def complete(tab, opts):
    el = [x for x in tab]
    pat = "".join(
        list(
            map(
                lambda x: x + r"\w*" if re.match(r"\w", x) else x,
                el,
            )
        )
    )
    try:
        opts = [x for x in opts if re.search(pat, x, re.IGNORECASE)]
    except Exception:
        opts = [x for x in opts if x.startswith(tab)]
    if not len(opts) or str.lower(tab) in list(map(str.lower, opts)):
        return ""
    cads = "|".join(opts[:5])
    if len(opts) > 5:
        cads += "|..."
    return "({0})".format(cads)


def chooseNext(string, array, length=0):
    return array[array.index(string) - (length or len(array)) + 1]
