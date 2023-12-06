def getEnv(augmented, bNiceMatrix):
    if not augmented and not bNiceMatrix:
        return "matrix"
    elif augmented and not bNiceMatrix:
        return "array"
    elif augmented and bNiceMatrix:
        return "NiceArray"
    else:
        return "NiceMatrix"


def getBraces(specialEnv, augmented):
    if specialEnv == "b" and augmented:
        return "\\left[", "\\right]"
    elif specialEnv == "B" and augmented:
        return "\\left\\{", "\\right\\}"
    elif specialEnv == "p" and augmented:
        return "\\left(", "\\right)"
    elif specialEnv == "v" and augmented:
        return "\\left|", "\\right|"
    elif specialEnv == "V" and augmented:
        return "\\left\\|", "\\right\\|"
    elif specialEnv == "d":
        return "\\left$1", "\\right$0"
    else:
        return "", ""


def getOpeningEnv(bNiceMatrix, augmented, specialEnv, env, cols):
    colLetter = "c" * (cols - 1)

    if augmented and not bNiceMatrix:
        return "\\begin{array}{" + colLetter + "|c}\n"
    elif augmented and bNiceMatrix:
        string = "\\begin{" + specialEnv + "NiceArray}"
        return string + "{" + colLetter + "|c}\n"
    elif not augmented and bNiceMatrix:
        string = "\\begin{" + specialEnv + "NiceMatrix}"
        return string + "[columns-width=auto]\n"
    else:
        return "\\begin{" + env + "}\n"


def getClosingEnv(bNiceMatrix, augmented, specialEnv, env):
    if augmented and not bNiceMatrix:
        return "\\end{array}"
    elif augmented and bNiceMatrix:
        return "\\end{" + specialEnv + "NiceArray}"
    elif not augmented and bNiceMatrix:
        return "\\end{" + specialEnv + "NiceMatrix}"
    else:
        return "\\end{" + env + "}"


def createMatrix(snip, match, bNiceMatrix=False):
    rows, cols = int(match.group(3)), int(match.group(4))
    specialEnv = match.group(2) or ""
    augmented = match.group(1)

    env = getEnv(augmented, bNiceMatrix)
    offset = cols + 1

    if specialEnv and specialEnv != "d":
        env = str(specialEnv) + env

    offset = cols + 1
    snip.buffer[snip.line] = ""

    openBrace, closeBrace = getBraces(specialEnv, augmented)

    finalStr = ""

    if not bNiceMatrix:
        finalStr = openBrace

    finalStr += getOpeningEnv(bNiceMatrix, augmented, specialEnv, env, cols)

    for i in range(rows):
        finalStr += "\t"
        rowValues = []
        for j in range(cols):
            rowValues.append("$" + str(i * cols + j + offset))

        finalStr += " & ".join(rowValues)
        finalStr += " \\\\\\\n"

    finalStr += getClosingEnv(bNiceMatrix, augmented, specialEnv, env)

    if not bNiceMatrix:
        finalStr += closeBrace

    snip.expand_anon(finalStr)
