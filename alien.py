import random
from species_data import NAMES,PLANETS,PLANET_SPECIES
from document import Document

class Alien:
    def __init__(s):
        s.name = random.choice(NAMES)
        s.claimed_planet = random.choice(PLANETS)

        correct_traits = PLANET_SPECIES[s.claimed_planet]
        s.eyes = correct_traits["eyes"]
        s.colour = correct_traits["colour"]
        s.limbs = correct_traits["limbs"]
        s.expiration_date = random.randint(2027, 2040)

        s.doc_type = random.choice(
            ["PASSPORT", "ID CARD", "STUDENT ID"],
        )[0]
        s.doc_id = random.randint(10000,999999)

        passport_limbs = s.limbs

        #45% chance to be an anomaly
        if random.random() < 0.45:
            anomaly = random.choice(["expiration_date","limbs"])
            if anomaly == "expiration_date":
                s.expiration_date = random.randint(2022,2025)
            elif anomaly == "limbs":
                other_limbs = [n for n in [2,4,6,8] if n != correct_traits["limbs"]]
                passport_limbs = random.choice(other_limbs)

        s.passport = Document(s.name, s.claimed_planet, s.expiration_date, passport_limbs)