from latex_.scopes import display_math
from sympy import latex

wolframscript_timeout_default = 10


def pre_process_text(text):
    return (
        text.replace("\\", "")
        .replace("^", "**")
        .replace("{", "(")
        .replace(
            "}",
            ")",
        )
    )


def pre_process_latex(text):
    return (
        text
        # .replace(r"\e", r" e")
        .replace(r"\d ", r"\,d")
        .replace(
            "\\textrm{d}",
            "d",
        )
    )


def process_latex(text):
    return text.replace(
        r"\, d",
        r"\textrm{d}",
    )


def get_block(form, snip):
    start = 0
    if display_math():
        status = 0
        for index, line in enumerate(snip.buffer[: snip.line]):
            if line == form:
                status = not status
                if status:
                    start = index

        if status:
            return (start, "\n".join(snip.buffer[start + 1: snip.line]))

    return ("", "")


def calculate_sympy(snip):
    index, block = get_block("Sympy", snip)
    snip.buffer[index: snip.line + 1] = [""]

    code = pre_process_text(block)

    tex = f"""
from sympy import *
from latex2sympy2 import *
x, y, z, t = symbols('x y z t')
k, m, n = symbols('k m n', integer = True)
f, g, h = symbols('f g h', cls = Function)
{code}"""

    result = ""

    sympy_result = {}
    exec(tex, sympy_result)
    rv = sympy_result["rv"] or block
    lrv = latex(rv)
    result = process_latex(lrv)

    snip.cursor.set(index, len(result))
    snip.buffer[index] = result
