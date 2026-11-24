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
        s.expiration_date = random.randint(2026, 2040)

        #45% chance to be an anomaly
        if random.random() < 0.45:
            anomaly = random.choice(["expiration_date","eyes","colour"])
            if anomaly == "expiration_date":
                s.expiration_date = random.randint(2022,2025)
            elif anomaly == "eyes":
                s.eyes += 1
            elif anomaly == "colour":
                s.colour = "orange"

        s.passport = Document(s.name, s.claimed_planet, s.expiration_date, s.limbs)
