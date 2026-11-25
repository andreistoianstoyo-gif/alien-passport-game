import random
from species_data import PLANET_SPECIES

#random rule generator
RULE = [
    "Check the passport expiration date",
    "Check the number of eyes",
    "Check the colour of the alien",
    "Check the number of limbs",
    "Check all passport and species details",
]


def generate_rules():
    return{
        "RULE":random.choice(RULE)
    }

def check_decision(alien,active_rule,player_approval):
    
    expect = PLANET_SPECIES[alien.passport.planet]
    is_check = True

    if active_rule == "Check the passport expiration date":
        is_check = not alien.passport.is_expired()
    elif active_rule == "Check the number of eyes":
        is_check = (alien.eyes == expect["eyes"])
    elif active_rule == "Check the colour of the alien":
        is_check = (alien.colour == expect["colour"])
    elif active_rule == "Check the colour of the limbs":
        is_check = (alien.limbs == expect["limbs"])
    else:
        is_check = (
            not alien.passport.is_expired()
            and alien.eyes == expect["eyes"]
            and alien.colour == expect["colour"]
            and alien.limbs == expect["limbs"]
        )
    return player_approval == is_check

