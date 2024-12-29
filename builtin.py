import re
from collections import OrderedDict


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


def writeRoman(num):
    roman = OrderedDict()

    roman[1000] = "m"
    roman[900] = "cm"
    roman[500] = "d"
    roman[400] = "cd"
    roman[100] = "c"
    roman[90] = "xc"
    roman[50] = "l"
    roman[40] = "xl"
    roman[10] = "x"
    roman[9] = "ix"
    roman[5] = "v"
    roman[4] = "iv"
    roman[1] = "i"

    def roman_num(num):
        for r in roman.keys():
            x, _ = divmod(num, r)
            yield roman[r] * x
            num -= r * x
            if num <= 0:
                break

    return "".join([a for a in roman_num(num)])
