from sympy import latex
from subprocess import check_output, TimeoutExpired
from re import sub

from latex_.scopes import display_math

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
        text.replace(r"\e", r" e")
        .replace(r"\d ", r"\,d")
        .replace(
            "\\textrm{d}",
            "d",
        )
    )


def process_latex(text):
    return sub(r"(\s|\W?)e(?=\W)", r"\g<1>\\e", text).replace(
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

    pre_define = """
from sympy import *
x, y, z, t = symbols('x y z t')
k, m, n = symbols('k m n', integer = True)
f, g, h = symbols('f g h', cls = Function)
"""

    sympy_result = {}
    exec(pre_define + pre_process_text(block), sympy_result)

    result = process_latex(latex(sympy_result["rv"] or ""))
    snip.cursor.set(index, len(result))
    snip.buffer[index] = result


def calculate_wolfram_string(
    string,
    from_latex=False,
    timeout=wolframscript_timeout_default,
):
    result = ""

    if from_latex:
        code = (
            'ToString[ToExpression["'
            + pre_process_latex(string).replace(
                "\\",
                "\\\\",
            )
            + '", TeXForm], TeXForm]'
        )
    else:
        code = "ToString[" + string + ", TeXForm]"

    try:
        result = check_output(
            ["wolframscript", "-code", code],
            encoding="utf-8",
            timeout=int(timeout),
        ).strip()
    except TimeoutExpired:
        result = ""

    return result


def calculate_wolfram(
    snip,
    from_latex=False,
    timeout=wolframscript_timeout_default,
):
    index, block = get_block("\\wolfram" if from_latex else "wolfram", snip)
    snip.buffer[index: snip.line + 1] = [""]

    result = process_latex(
        calculate_wolfram_string(block, from_latex, timeout),
    )

    snip.cursor.set(index, len(result))
    snip.buffer[index] = result
