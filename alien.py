import random
from species_data import PLANETS,PLANETS_SPECIES,generate_alien_name
from document import Document

ALL_COLOURS = ["green", "purple", "blue", "yellow", "red", "orange", "pink"]
ALL_EYE_COUNTS = [1,2,3,4,6]
MOUTHS = ["smile", "fangs", ":o mouth", "wavy","flat","smirk"]

class Alien:
    def __init__(s):
        s.name = generate_alien_name()
        s.claimed_planet = random.choice(PLANETS)

        correct_traits = PLANETS_SPECIES[s.claimed_planet]
        s.eyes = correct_traits["eyes"]
        s.limbs = correct_traits["limbs"]
        s.colour = correct_traits["colour"]
        s.head = correct_traits.get("head", "round")
        s.accessory = correct_traits.get("accessory", "antennae")
        s.mouth = random.choice(MOUTHS)
        s.expiration_date = random.randint (2027, 2040)

        s.doc_type = random.choices(
            ["PASSPORT", "ID CARD", "STUDENT ID"],
            weights = [75,15,10],
        )[0]
        s.doc_id = random.randint(10000,999999)

        passport_limbs = s.limbs

        if random.random() < 0.45:
            anomaly = random.choice(["expiration_date", "limbs", "eyes", "colour"])
            if anomaly == "expiration_date":
                s.expiration_date = random.randint(2022,2026)
            elif anomaly == "limbs":
                other_limbs = [n for n in [2,4,6,8] if n != correct_traits["limbs"]]
                if random.random() < 0.5:
                    passport_limbs = random.choice(other_limbs)
                else:
                    s.limbs = random.choice(other_limbs)
                    passport_limbs = s.limbs
            elif anomaly == "eyes":
                other_eyes = [e for e in ALL_EYE_COUNTS if e != correct_traits["eyes"]]
                s.eyes = random.choice(other_eyes)
            elif anomaly == "colour":
                other_colour  = [c for c in ALL_COLOURS if c != correct_traits["colour"]]
                s.colour = random.choice(other_colour)

        s.passport = Document(s.name, s.claimed_planet, s.expiration_date, passport_limbs)

        s.booth_sprite = None
        s.photo_sprite = None