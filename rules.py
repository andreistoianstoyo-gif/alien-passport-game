import random

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