#############
#  Accents  #
#############

specialBarHatVec = ["i", "j"]
mapBarHatVec = {
    "bar": "\\overline",
    "hat": "\\widehat",
    "vec": "\\overrightarrow",
}
bars = ["\\bar", "\\overline"]
hats = ["\\hat", "\\widehat"]
vecs = ["\\vec", "\\overrightarrow"]

###########
#  Logic  #
###########

existsTermsCycle = ["exists", "exists"]
ands = ["land", "bigwedge"]
ors = ["lor", "bigvee"]

###############
#  Operators  #
###############

plusMinus = ["\\pm", "\\mp"]

#################
#  Parenthesis  #
#################

opening = ["(", "[", r"\{"]
closing = [")", "]", r"\}"]
vert = ["\\vert", "\\Vert"]

##############
#  Pointers  #
##############

leftArrows = [
    "\\leftarrow",
    "\\gets",
    "\\longleftarrow",
    "\\Leftarrow",
    "\\Longleftarrow",
    "\\impliedby",
]
rightArrows = [
    "\\rightarrow",
    "\\to",
    "\\longrightarrow",
    "\\Rightarrow",
    "\\Longrightarrow",
    "\\implies",
]
leftrightArrows = [
    "\\longleftrightarrow",
    "\\Leftrightarrow",
    "\\Longleftrightarrow",
    "\\iff",
]

###############
#  Relations  #
###############

nornot = ["", "n"]

#############
#  Symbols  #
#############

dots = ["", "c", "v", "d"]
infties = ["", "-", "+"]

###########
#  Unitx  #
###########

units = {
    "mm": r"\millimeter",
    "cm": r"\centimeter",
    "dm": r"\decimeter",
    "in": r"\inch",
    "ft": r"\foot",
    "yd": r"\yard",
    "m": r"\meter",
    "km": r"\kilometer",
    "mi": r"\mile",
    "mph": r"\mile\per\hour",
    "kph": r"\kilometer\per\hour",
    "n": r"\newton",
    "rad": r"\radian",
    "deg": r"\degree",
    "l": r"\liter",
    "ml": r"\milliliter",
    "gal": r"\gallon",
    "ms": r"\millisecond",
    "s": r"\second",
    "min": r"\minute",
    "hr": r"\hour",
    "d": r"\day",
    "wk": r"\week",
    "mos": r"\month",
    "yr": r"\year",
    "mg": r"\milligram",
    "g": r"\gram",
    "oz": r"\ounce",
    "lb": r"\pound",
    "kg": r"\kilogram",
    "t": r"\ton",
    "sq": r"\squared",
    "cb": r"\cubed",
    "per": r"\per",
}

#############
#  Spacing  #
#############

spaces = ["\\qquad", "\\quad", "\\,", "\\:", "\\;", "\\!", "\\ "]
