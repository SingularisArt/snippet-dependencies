import re

from latex_.scopes import displayMath
from sympy import latex


def preProcessText(text):
    return (
        text.replace("\\", "")
        .replace("^", "**")
        .replace("{", "(")
        .replace(
            "}",
            ")",
        )
    )


def preProcessLatex(text):
    return (
        text
        # .replace(r"\e", r" e")
        .replace(r"\d ", r"\,d")
        .replace(
            "\\textrm{d}",
            "d",
        )
    )


def processLatex(text):
    return text.replace(
        r"\, d",
        r"\textrm{d}",
    )


def getBlock(form, snip):
    start = 0
    if displayMath():
        status = 0
        for index, line in enumerate(snip.buffer[: snip.line]):
            if line == form:
                status = not status
                if status:
                    start = index

        if status:
            return (start, "\n".join(snip.buffer[start + 1: snip.line]))

    return ("", "")


def expandBrackets(string):
    lBrackets = ["(", "[", r"\{"]
    rBrackets = [")", "]", r"\}"]

    for bracket in lBrackets:
        pattern = r"(?<!\\left)" + re.escape(bracket)
        replaceString = r"\\left" + bracket
        string = re.sub(pattern, replaceString, string)

    for bracket in rBrackets:
        pattern = r"(?<!\\right)" + re.escape(bracket)
        replaceString = r"\\right" + bracket
        string = re.sub(pattern, replaceString, string)

    return string


def calculateSympy(snip):
    index, block = getBlock("Sympy", snip)
    snip.buffer[index: snip.line + 1] = [""]

    code = preProcessText(block)

    tex = f"""
from sympy import *
from latex2sympy2 import *
x, y, z, t = symbols('x y z t')
k, m, n = symbols('k m n', integer = True)
f, g, h = symbols('f g h', cls = Function)
{code}"""

    result = ""

    sympyResult = {}
    exec(tex, sympyResult)
    rv = sympyResult["rv"] or block
    lrv = latex(rv)
    result = processLatex(lrv)

    snip.cursor.set(index, len(result))
    snip.buffer[index] = result
