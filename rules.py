import random
from alien import Alien
from species_data import PLANETS_SPECIES

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

def evaluate_encounter(alien: Alien, active_rule: str, dialogue: dict):
    if alien.doc_type != "PASSPORT":
        return False, f"Wrong! Invalid doc type: {alien.doc_type} stupid ahh"

    if dialogue["is_lying"]:
        return False, "Wrong! The alien lied to you!"

    if alien.passport.limbs != alien.limbs:
        return False, f"Wrong! Passport says {alien.passport.limbs} limbs, alien has {alien.limbs}!"

    if alien.passport.planet != alien.claimed_planet:
        return False, f"Wrong! Passport planet doesn't match!"

    expect = PLANETS_SPECIES[alien.passport.planet]

    if active_rule == "Check the passport expiration date":
        if alien.passport.is_expired():
            return False, f"Wrong, the passport is expired...(sad)"
        return True, ""

    if active_rule == "Check the number of eyes":
        if alien.eyes != expect["eyes"]:
            return False, f"Wrong, {alien.passport.planet} aliens have {expect['eyes']}eyes!"
        return True, ""
    
    if active_rule == "Check the colour of the alien":
        if alien.colour != expect["colour"]:
            return False, f"Wrong, {alien.passport.planet} aliens are {expect['colour']}!"
        return True, ""

    if active_rule == "Check the number of limbs":
        if alien.limbs != expect["limbs"] or alien.passport.limbs != expect["limbs"]:
            return False, f"Wrong, {alien.passport.planet} aliens have {expect['limbs']} limbs!"
        return True, ""

    if alien.passport.is_expired():
        return False, f"Wrong! The passport expired in {alien.passport.expiration_date}!"
    if alien.passport.limbs != expect["limbs"] or alien.limbs != expect ["limbs"]:
        return False, f"Wrong! {alien.passport.planet} aliens have {expect['limbs']} limbs!"
    if alien.eyes != expect["eyes"]:
        return False, f"Wrong! {alien.passport.planet} aliens have {expect['eyes']} eyes!"
    if alien.colour != expect["colour"]:
        return False, f"Wrong! {alien.passport.planet} aliens are {expect['colour']}!"

    return True, ""

def check_decision(alien:Alien, active_rule:str , player_approval: bool):
    is_valid, _ = evaluate_encounter(alien, active_rule, {"is_lying":False})
    return player_approval == is_valid
