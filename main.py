import pygame
import random

pygame.init()
LENGTH, HEIGHT = 1280,720
screen = pygame.display.set_mode((LENGTH,HEIGHT))
pygame.display.set_caption("Alien Passport Control")
clock = pygame.time.Clock()
running = True
dt = 0

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

passport_rect = pygame.Rect(100,30,420,480)
approve_button = pygame.Rect(350,625,225,60)
deny_button = pygame.Rect(700,625,225,60)
rules_rect = pygame.Rect(1000,50,225,550)
font_button = pygame.font.SysFont("arial", 28, bold = True)
font_title = pygame.font.SysFont("arial", 24, bold = True)
rule_font = pygame.font.SysFont("arial",16, bold = True)

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
background = (25,28,38)

while running == True:
    screen.fill(background)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if approve_button.collidepoint(event.pos):
                current_alien = generate_alien()
                pygame.draw.rect(screen,(1,50,32),approve_button)
                print("Alien APPROVED!")
            elif deny_button.collidepoint(event.pos):
                print("Alien DENIED")
                current_alien = generate_alien()
    pygame.draw.rect(screen, (235,230,215), passport_rect)
    pygame.draw.rect(screen,("green"),approve_button)
    pygame.draw.rect(screen,("red"),deny_button)
    pygame.draw.rect(screen,("blue"),rules_rect)

    #BUTTONS
    text_approve = font_button.render("APPROVED", True, "white")
    screen.blit(text_approve,(approve_button.x + 35, approve_button.y + 15))
    text_deny = font_button.render("DENIED", True, "white")
    screen.blit(text_deny,(deny_button.x + 60, deny_button.y + 15))
    #DAILY RULES
    daily_rules = font_title.render("DAILY RULES", True, "yellow")
    screen.blit(daily_rules,(rules_rect.x + 25, rules_rect.y + 10))
    rule_one = rule_font.render(f"RULE NO.1: {current_rule['RULE']}",True,"yellow")
    screen.blit(rule_one,(rules_rect.x + 15, rules_rect.y + 40))
    #PASSPORT
    passport_title = font_title.render("GALACTIC PASSPORT",True,"black")
    screen.blit(passport_title,(passport_rect.x+75,passport_rect.y + 15))
    alien_name = font_title.render(f"Name: {current_alien['name']}",True,"black")
    screen.blit(alien_name,(passport_rect.x+25,passport_rect.y+60))
    alien_planet = font_title.render(f"Planet: {current_alien['planet']}",True,"black") 
    screen.blit(alien_planet,(passport_rect.x+25,passport_rect.y+120))
    alien_passport_expiration_date = font_title.render(f"Expiration date: {current_alien['expires']}",True,"black")
    screen.blit(alien_passport_expiration_date,(passport_rect.x+25,passport_rect.y+180))
    
   
    pygame.display.flip()

    dt = clock.tick(60)/1000

pygame.quit()