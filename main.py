import pygame
from alien import Alien
from rules import generate_rules,check_decision
from ui import PixelButton, pixel_8_bit_border, not_unbound_text

pygame.init()
LENGTH, HEIGHT = 1280,720
screen = pygame.display.set_mode((LENGTH,HEIGHT))
pygame.display.set_caption("RuAlien?")
clock = pygame.time.Clock()

#the fonts duh
font = pygame.font.Font("assets/fonts/PixelifySans-VariableFont_wght.ttf",28)
big_font = pygame.font.Font("assets/fonts/PixelifySans-VariableFont_wght.ttf",40)
rule_font = pygame.font.Font("assets/fonts/PixelifySans-VariableFont_wght.ttf",24)
small_font = pygame.font.Font("assets/fonts/PixelifySans-VariableFont_wght.ttf",18)
field_font = pygame.font.Font("assets/fonts/PixelifySans-VariableFont_wght.ttf",16)

#da sprites
alien_img = pygame.image.load("assets/sprites/alien.png").convert_alpha()
alien_img = pygame.transform.scale(alien_img, (192,192))
big_alien_image = pygame.transform.scale(alien_img, (256,256))

raw_passport = pygame.image.load("assets/sprites/passport.png").convert_alpha()
passport_image = pygame.transform.scale_by(raw_passport, 3)
passport_shadow_image = pygame.mask.from_surface(passport_image).to_surface(
    setcolor=(10,12,18,255),unsetcolor=(0,0,0,0))

passport_width, passport_height = passport_image.get_size()
passport_rect = pygame.Rect(60,110,passport_width, passport_height)
    
try:
    raw_cover = pygame.image.load("assets/sprites/passport_cover.png").convert_alpha()
    cover_image = pygame.transform.scale_by(raw_cover, 3)
except FileNotFoundError:
    cover_image = pygame.Surface((108,144), pygame.SRCALPHA)
    pixel_8_bit_border(cover_image,pygame.Rect(0,0,108,144),(32,45,75), (20,28,48), notch = 4, border = 4)
    pygame.draw.rect(cover_image,(240,200,50), (36,42,36,36), 4)
             
mini_passport_rect = cover_image.get_rect(topleft=(140,515))

rules_icon = pygame.image.load("assets/sprites/rules.png").convert_alpha()
rules_icon = pygame.transform.scale(rules_icon,(192,192))
rules_icon_rect = rules_icon.get_rect(topright=(1305,0))

#buttuhs
approve_button = PixelButton(300,605,270,90,"APPROVE", big_font, (0,200,0),(50,240,100), (0,100,32))
deny_button = PixelButton(700,605,280,90, "DENY", big_font, (200,0,0), (240,50,100), (100,0,32))

#state of the game
current_alien = Alien()
current_rule = generate_rules["RULE"]
score = 0
strikes = 0
feedback_text = ""
feedback_colour = "white"
feedback_timer = 0.0

#ui windows settings
passport_is_opened = False
passport_scale = 0.0
dragging_passport = False
drag_offset = (0,0)

rules_is_opened = False
rules_scale = 0.0

running = True
while running:
    dt = clock.tick(60)/ 1000
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:
                rules_is_opened = not rules_is_opened

            if event.key == pygame.K_p:
                passport_is_opened = not passport_is_opened
                dragging_passport = False

            if event.key == pygame.K_ESCAPE:
                passport_is_opened = False
                rules_is_opened = False
                dragging_passport = False

            if event.key == pygame.K_space:
                current_alien = Alien()
                current_rule = generate_rules()["RULE"]
                passport_is_opened = False
                dragging_passport = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if rules_icon_rect.collidepoint(event.pos):
                rules_is_opened = not rules_is_opened

            if passport_is_opened and passport_scale > 0.9:
                close_button_rect = pygame.Rect = (passport_rect.right - 45, passport_rect.y + 10,34,34)
                title_bar_rect = pygame.Rect(passport_rect.x, passport_rect.y, passport_width - 50, 54)

                if close_button_rect.collidepoint(event.pos):
                    passport_is_opened = False
                    dragging_passport = False
                elif title_bar_rect.collidepoint(event.pos):
                    dragging_passport = True
                    drag_offset = (passport_rect - event.pos[0],passport_rect.y - event.pos[1])
                elif mini_passport_rect.collidepoint(event.pos):
                    passport_is_opened = False
            elif mini_passport_rect.collidepoint(event.pos):
                passport_is_opened = True

        if event.type == pygame.MOUSEBUTTONUP and event.button == [1]:
             dragging_passport = False

        if event.type == pygame.MOUSEMOTION and dragging_passport:
            passport_rect.x = event.pos[0] + drag_offset[0]
            passport_rect.y = event.pos[1] + drag_offset[1]
            passport_rect.clamp_id(pygame.Rect(0,0, LENGTH, HEIGHT))

        #checking da decision on approve or deny
        if approve_button.clicking(event) or deny_button.clicking(event):
            player_approval = approve_button.clicking(event)
            if check_decision(current_alien, current_rule, player_approval):
                score += 1
                feedback_text = "APPROVED / DENIED CORRECTLY! +1(nice job bro)"
                feedback_colour = (80,240,120)
            else:
                strikes += 1
                feedback_text = "WRONG DECISION! (dumbass)"
                feedback_colour = (240,70,90)

            feedback_timer = 1.6
            current_alien = Alien()
            current_rule = generate_rules()["RULE"]
            passport_is_opened = False
            dragging_passport = False
             