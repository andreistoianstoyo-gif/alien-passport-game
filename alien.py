import random
from species_data import NAMES,PLANETS,PLANET_SPECIES
from document import Document

class Alien:
    def __init__(self):
        self.name = random.choice(NAMES)
        self.claimed_planet = random.choice(PLANETS)

        correct_traits = PLANET_SPECIES[self.claimed_planet]
