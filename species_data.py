import random

FIRST_NAMES = [
    "Zyx", "Pip", "Bloop", "Gorgon", "Vela", "Beene","Krag", "Vex", "Nyx", "Nory"
    "Zorp", "Quix", "Tlop", "Tali", "Morb", "Florp", "Drax", "Styla", "Rix", "Kale", "Lavi"
    "Olo", "Mori", "Kael", "Klarp", "Bris", "Plip", "Tke", "Xeno", "Vornak", "Luma", "Plorb"
    "Jole", "Gar",
]

LAST_NAMES = [
        "Kor","Xenox","De Lerak","Nueva","Busi", "Vorn", "Zyrax", "Murla"
        "Kroll", "Naschov","Prax","Jonie", "Splik", "Torak", "Krix", "Daro"
        "Bendu", "Dalv", "Qir", "Lap",
]

NAME_SUFFIEXS =  [
    "", "", "", "", "", "Jr", "III", "II", "IV","-7"
]

PLANETS = ["Mars", "Zorgon", "Volor", "Darolan", "Titan", "Pluto", "Alpha-Qent", "Pandora", "Kira"]

PLANETS_SPECIES = {
    "Mars": {"eyes":2, "colour":"green", "limbs":4, "head":"round", "accessory":"antennae"},
    "Zorgon":{"eyes":2, "colour":"purple", "limbs":6, "head":"sqare", "accessory":"horns"},
    "Volor":{"eyes":1, "colour":"orange", "limbs":2, "head":"pear", "accessory":"crest"},
    "Darolan":{"eyes":6, "colour":"yellow", "limbs":2, "head":"wide", "accessory":"ears"},
    "Titan":{"eyes":2, "colour":"red", "limbs":8, "head":"oval", "accessory":"horns"},
    "Pluto":{"eyes":4, "colour":"orange", "limbs":4, "head":"pear", "accessory":"ears"},
    "Alpha-Qent":{"eyes":3, "colour":"blue", "limbs":6, "head":"round", "accessory":"antennae"},
    "Pandora":{"eyes":2, "colour":"blue", "limbs":4, "head":"oval", "accessory":"ears"},
    "Kira":{"eyes":4, "colour":"pink", "limbs":6, "head":"wide", "accessory":"crest"},
}

def generate_alien_name():
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    name_suffixes = random.choice(NAME_SUFFIEXS)

    if name_suffixes:
        if name_suffixes.startswith("-"):
            return f"{first_name} {last_name}{name_suffixes}"
        return f"{first_name} {last_name} {name_suffixes}"
    return f"{first_name} {last_name}"