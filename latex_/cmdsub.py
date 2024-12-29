from builtin import writeRoman
from .variables import specialBarHatVec, mapBarHatVec, units

commandMapping = [
    "🚀",
    "🚁",
    "🚂",
    "🚃",
    "🚄",
    "🚅",
    "🚆",
    "🚇",
    "🚈",
    "🚉",
    "🚊",
    "🚋",
    "🚌",
    "🚍",
    "🚎",
    "🚏",
]


def replaceCommands(target, commands, replacements):
    for i in range(len(commands)):
        target = target.replace(commands[i], replacements[i])
    return target


def findAndReplace(target, bracketnum, replace_func):
    string = list(target)
    depth = braces = 0
    for i in range(len(string) - 1, -1, -1):
        if string[i] == "}":
            depth += 1
        elif string[i] == "{":
            depth -= 1
        elif braces == bracketnum:
            if not depth:
                try:
                    string[i] = replace_func(string[i])
                    break
                except ValueError:
                    pass
        braces += 0 if depth else 1
    return "".join(string)


def commandCycle(target, commands, bracketnum=1):
    command_map = commandMapping[: len(commands)]
    target = replaceCommands(target, commands, command_map)
    target = findAndReplace(
        target,
        bracketnum,
        lambda x: x,
    )
    target = replaceCommands(target, command_map, commands)
    return target


def commandSwap(target, command_1, command_2, bracketnum=1):
    target = target.replace(command_1, "🚀").replace(command_2, "🚁")
    target = findAndReplace(target, bracketnum, lambda x: x)
    return target.replace("🚀", command_1).replace("🚁", command_2)


def createTable(snip, match):
    s = snip.buffer[snip.line]
    rows, cols = int(match.group(2)), int(match.group(3))
    offset = cols + 1
    old_spacing = s[: s.rfind("\t") + 1]
    snip.buffer[snip.line] = ""
    text_type = match.group(1)

    column_format_parts = []
    for i in range(cols):
        if text_type:
            column_format_parts.append(f"${i + 1}:{text_type}")
        else:
            column_format_parts.append(f"${i + 1}")

    column_format = "|" + "|".join(column_format_parts) + "|"
    final_str = f"{old_spacing}\\begin{{tabular}}{{{column_format}}}\n"

    for i in range(rows):
        final_str += f"{old_spacing}\t"
        row_values = ["$" + str(i * cols + j + offset) for j in range(cols)]
        final_str += " & ".join(row_values) + " \\\\\\\n"

    final_str += f"{old_spacing}\\end{{tabular}}$0"
    snip.expand_anon(final_str)


def createProblemSolution(snip, match):
    snip.buffer[snip.line] = ""

    finalStr = "\\begin{problem}\n"
    finalStr += "\t\\begin{enumerate}\n"

    for i in range(int(match.group(1))):
        finalStr += "\t\t\\item $" + str(i + 1) + "\n"

        if i < int(match.group(1)) - 1:
            finalStr += "\n"

    finalStr += "\t\\end{enumerate}\n"
    finalStr += "\\end{problem}\n"

    finalStr += "\n"

    for i in range(int(match.group(1))):
        numeral = writeRoman(i + 1)

        finalStr += f"\\begin{{proof}}[Solution to ({numeral})]\n"
        finalStr += "\t$" + str(i + 1 + int(match.group(1))) + "\n"
        finalStr += "\\end{proof}\n"

        if i < int(match.group(1)) - 1:
            finalStr += "\n"

    snip.expand_anon(finalStr)

def addRow(snip, match):
    s = snip.buffer[snip.line]

    rowLen = int(match.group(1))
    oldSpacing = s[: s.rfind("\t") + 1]
    snip.buffer[snip.line] = ""

    finalStr = oldSpacing
    finalStr += " & ".join(["$" + str(j + 1) for j in range(rowLen)])
    finalStr += " \\\\\\"

    snip.expand_anon(finalStr)


def complete(t, opts):
    if t:
        opts = [m[len(t):] for m in opts if m.startswith(t)]
    if len(opts) == 1:
        return opts[0]

    return "(" + "|".join(opts) + ")"


def barHatVec(target, word, subscript=""):
    return (
        "\\"
        + target
        + "{"
        + ("\\" + word + "math" if word in specialBarHatVec else word)
        + "}"
        + (subscript or "")
    )


def longBarHatVec(target, word, subscript=""):
    return mapBarHatVec[target] + "{" + word + "}" + (subscript or "")


def expandUnit(string):
    new_string = []

    string_split = string.replace("  ", r" per ").split()

    for str in string_split:
        if str not in units:
            new_string.append(f"\\{str}")
        else:
            for unit in units:
                if str == unit:
                    new_string.append(units[unit])

    return "".join(new_string)
