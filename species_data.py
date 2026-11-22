import pygame
import random

#random alien generator
NAMES = ["Zyx Kor","Pip Xenox","Bloop Lesan","Gorgon Delerak","Vela Nueva","Beene Buzy"]
PLANETS = ["Mars","Zorgon-67","Volor","Darialand","Titan"]

def generate_alien():
    return{
        "name": random.choice(NAMES),
        "planet": random.choice(PLANETS),
        "expires": random.randint(2024,2040)
    }
current_alien = generate_alien()

#random rule generator
RULE = [
    "Check the passport availability",
    "Check the number of eyes",
    "Check the colour of the alien",
    "Check the number of members",
    "Check the species accordingly to the planet"
]
def generate_rules():
    return{
        "RULE":random.choice(RULE)
    }
current_rule = generate_rules()