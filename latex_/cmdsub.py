command_mapping = [
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


def replace_commands(target, commands, replacements):
    for i in range(len(commands)):
        target = target.replace(commands[i], replacements[i])
    return target


def find_and_replace(target, bracketnum, replace_func):
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


def command_cycle(target, commands, bracketnum=1):
    command_map = command_mapping[: len(commands)]
    target = replace_commands(target, commands, command_map)
    target = find_and_replace(
        target,
        bracketnum,
        lambda x: x,
    )
    target = replace_commands(target, command_map, commands)
    return target


def command_swap(target, command_1, command_2, bracketnum=1):
    target = target.replace(command_1, "🚀").replace(command_2, "🚁")
    target = find_and_replace(target, bracketnum, lambda x: x)
    return target.replace("🚀", command_1).replace("🚁", command_2)


def create_table(snip, match):
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


def add_row(snip, match):
    s = snip.buffer[snip.line]

    rowLen = int(match.group(1))
    oldSpacing = s[: s.rfind("\t") + 1]
    snip.buffer[snip.line] = ""

    finalStr = oldSpacing
    finalStr += " & ".join(["$" + str(j + 1) for j in range(rowLen)])
    finalStr += " \\\\\\"
    snip.expand_anon(finalStr)


def create_matrix(snip, match):
    rows, cols = int(match.group(3)), int(match.group(4))
    specialEnv = match.group(2)
    augmented = match.group(1)

    env = "matrix"
    offset = cols + 1

    if specialEnv:
        env = str(specialEnv) + env

    offset = cols + 1
    snip.buffer[snip.line] = ""

    openBrace, closeBrace = "", ""
    if specialEnv == "b" and augmented:
        openBrace, closeBrace = "\\left[", "\\right]"
    elif specialEnv == "B" and augmented:
        openBrace, closeBrace = "\\left\\{", "\\right\\}"
    elif specialEnv == "p" and augmented:
        openBrace, closeBrace = "\\left(", "\\right)"
    elif specialEnv == "v" and augmented:
        openBrace, closeBrace = "\\left|", "\\right|"
    elif specialEnv == "V" and augmented:
        openBrace, closeBrace = "\\left\\|", "\\right\\|"
    elif specialEnv == "d":
        openBrace, closeBrace = "\\left$1", "\\right$0"

    colLetter = "c" * (cols - 1)
    finalStr = openBrace

    if augmented:
        finalStr += "\\begin{array}{" + colLetter + "|c}\n"
    elif specialEnv == "d":
        finalStr += "\\begin{matrix}\n"
    else:
        finalStr += "\\begin{" + env + "}\n"

    for i in range(rows):
        finalStr += "\t"
        rowValues = []
        for j in range(cols):
            rowValues.append("$" + str(i * cols + j + offset))

        finalStr += " & ".join(rowValues)
        finalStr += " \\\\\\\n"

    if augmented:
        finalStr += "\\end{array}"
    elif specialEnv == "d":
        finalStr += "\\end{matrix}"
    else:
        finalStr += "\\end{" + env + "}"

    finalStr += closeBrace

    snip.expand_anon(finalStr)


def complete(t, opts):
    if t:
        opts = [m[len(t):] for m in opts if m.startswith(t)]
    if len(opts) == 1:
        return opts[0]

    return "(" + "|".join(opts) + ")"
