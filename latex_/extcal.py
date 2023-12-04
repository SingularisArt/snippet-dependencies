from latex_.scopes import display_math
from sympy import *
from latex2sympy2 import latex2sympy
from re import sub
from subprocess import check_output, TimeoutExpired

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
        .replace("\\textrm{d}", "d")
    )


def process_latex(text):
    return sub(r"(\s|\W?)e(?=\W)", r"\g<1>\\e", text).replace(r"\, d", r"\d ")
