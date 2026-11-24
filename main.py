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
current_rule = generate_rules()["RULE"]
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
                close_button_rect = pygame.Rect(passport_rect.right - 45, passport_rect.y + 10,34,34)
                title_bar_rect = pygame.Rect(passport_rect.x, passport_rect.y, passport_width - 50, 54)

                if close_button_rect.collidepoint(event.pos):
                    passport_is_opened = False
                    dragging_passport = False
                elif title_bar_rect.collidepoint(event.pos):
                    dragging_passport = True
                    drag_offset = (passport_rect.x - event.pos[0],passport_rect.y - event.pos[1])
                elif mini_passport_rect.collidepoint(event.pos):
                    passport_is_opened = False
            elif mini_passport_rect.collidepoint(event.pos):
                passport_is_opened = True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
             dragging_passport = False

        if event.type == pygame.MOUSEMOTION and dragging_passport:
            passport_rect.x = event.pos[0] + drag_offset[0]
            passport_rect.y = event.pos[1] + drag_offset[1]
            passport_rect.clamp_ip(pygame.Rect(0,0, LENGTH, HEIGHT))

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

    #BACKGROUND
    screen.fill((58,68,88))

    #centeh window
    booth_rect = pygame.Rect(415,35,450,425)
    pixel_8_bit_border(screen, booth_rect, (28,34,46), (35,42,56), notch = 8, border = 8)
    pygame.draw.line(screen, (42,50,66), (450,70), (520,140), 4)
    pygame.draw.line(screen, (42,50,66), (475,70), (535,130), 2)

    alien_booth_rect = big_alien_image.get_rect(center=(640,275))
    screen.blit(big_alien_image,alien_booth_rect)

    #table
    pygame.draw.rect(screen, (42,48,62), (0,460,1280,260))
    pygame.draw.rect(screen, (80,90,110), (0,460,1280,16))
    pygame.draw.line(screen, (20,24,32), (0,476), (1280,476), 4)
    for bolts in range(40,1280,160):
        pygame.draw.rect(screen, (35,40,45),(bolts, 465,6,6))

    #passport on the table
    hovering = -5 if mini_passport_rect.collidepoint(mouse_pos) else 0
    screen.blit(cover_image, (mini_passport_rect.x, mini_passport_rect.y + hovering))

    #approve/deny buttohs
    mouse_pressed_true = pygame.mouse.get_pressed()
    approve_button.draw(screen,mouse_pos,mouse_pressed_true)
    deny_button.draw(screen, mouse_pos, mouse_pressed_true)

    #HUD (scores and all of that blah-blah)
    hud_text = rule_font.render(f"SCORE:{score} | STRIKES: {strikes}/3", True, "white")
    screen.blit(hud_text, (40,40))

    if feedback_timer > 0:
        feedback_timer -= dt
        feedback_surface = rule_font.render(feedback_text, True, feedback_colour)
        screen.blit(feedback_surface, feedback_surface.get_rect(centerx= 640, y=10))

    #daily rules things
    if rules_icon_rect.collidepoint(mouse_pos):
        screen.blit(rules_icon, (rules_icon_rect.x, rules_icon_rect.y - 3))
    else:
        screen.blit(rules_icon, rules_icon_rect)

    target_scale = 1.0 if rules_is_opened else 0.0
    rules_scale += (target_scale - rules_scale) * 20 * dt

    if rules_scale > 0.05:
        RULES_WIDTH, RULES_HEIGHT = 290,480
        TRANSPARENT_BORDER = 14
        rules_surface = pygame.Surface(RULES_WIDTH + 15, RULES_HEIGHT + 15 + TRANSPARENT_BORDER)
            
        pygame.draw.rect(rules_surface, (15,17,24), (15,15 + TRANSPARENT_BORDER,RULES_WIDTH,RULES_HEIGHT),0,17)
        pygame.draw.rect(rules_surface, (0,190,230),(0, TRANSPARENT_BORDER, RULES_WIDTH,RULES_HEIGHT),0,17)
        pygame.draw.rect(rules_surface, (10,75,220), (0,TRANSPARENT_BORDER, RULES_WIDTH+3, RULES_HEIGHT+3),7,20)

        rules_title = font.render("DAILY RULES", True, "black")
        rules_title_rect = rules_title.get_rect(centerx = RULES_WIDTH // 2, y = 20 +TRANSPARENT_BORDER)
        rules_surface.blit(rules_title, rules_title_rect)
        pygame.draw.line(rules_surface, (12,17,24), (25,55 + TRANSPARENT_BORDER),(RULES_WIDTH - 25, 55 + TRANSPARENT_BORDER),3)
        pygame.draw.line(rules_surface, (200,200,0), (100,3 + TRANSPARENT_BORDER),(RULES_WIDTH - 100,3 + TRANSPARENT_BORDER),7)
        pygame.draw.line(rules_surface, (220,220,0), (100, TRANSPARENT_BORDER),(RULES_WIDTH-100, TRANSPARENT_BORDER),12)

        not_unbound_text(
            rules_surface,
            f"RULE 1: {current_rule}",
            rule_font,
            "black",
            pygame.Rect(0,0,RULES_WIDTH, RULES_HEIGHT),
            75,
        )

        NEW_WIDTH = max(1, int(RULES_WIDTH * rules_scale))
        NEW_HEIGHT = max(1,int(RULES_HEIGHT * rules_scale))
        scaled_panel = pygame.transform.scale(rules_surface, (NEW_WIDTH, NEW_HEIGHT))
        scaled_rect = scaled_panel.get_rect(topright=(1250,30))
        screen.blit(scaled_panel,scaled_rect)

    #PASSPORTTTTTTT
    target_idk_scale = 1.0 if passport_is_opened else 0.0
    passport_scale += (target_idk_scale - passport_scale) * 20 * dt

    if passport_scale > 0.05:
        passport_surface = pygame.Surface((passport_width + 12, passport_height + 12), pygame.SRCALPHA)
        passport_surface.blit (passport_shadow_image, (10,10))
        passport_surface.blit (passport_image, (0,0))

        title_text = font.render("GALACTIC PASSPORT", True, (240,210,60))
        passport_surface.blit(title_text(95,10))

        mini_photo = pygame.transform.scale(alien_img, (96,96))
        passport_surface.blit(mini_photo, (22,68))

        passport_surface.blit(small_font.render("CLASS : TRANSIT", True, (30,34,42)), (270,66))
        passport_surface.blit(small_font.render("DOCUMENT ID: #13565", True, (30,34,42)), (270,86))
        passport_surface.blit(small_font.render("SECTOR: OUTER", True, (30,34,42)), (270,106))

        passport_surface.blit(field_font.render(f"NAME: {current_alien.passport.name}",True,"black"), (155,143))
        passport_surface.blit(field_font.render(f"PLANET: {current_alien.passport.planet}", True, "black"), (34,173))
        passport_surface.blit(field_font.render(f"EXPIRES : {current_alien.passport.expiration_date}", True, "black"), (34,202))

        bars = 260
        for width in [3,3,2,2,4,2,4,6,3,4,5,3,2,2,2,3,4,4,2,2,3,5,2]:
            pygame.draw.rect(passport_surface, "black", (bars, 265, width, 36))
            bars += width + 4

        x_button_close_rect = pygame.Rect(passport_width - 45 , 10, 34, 34)
        global_close_button = x_button_close_rect.move(passport_rect.x, passport_rect.y)

        x_button_background = (240,60,80) if global_close_button.collidepoint(mouse_pos) else (185,30,40)
        pygame.draw.rect(passport_surface, x_button_background, x_button_close_rect,0,18)
        pygame.draw.rect(passport_surface, (255,255,255), x_button_close_rect,2,18)
        x_button_close_text = small_font.render("X", True, "white")
        passport_surface.blit(x_button_close_text, x_button_close_text.get_rect(center =x_button_close_rect.center))

        variable_x = mini_passport_rect.x + (passport_rect.x - mini_passport_rect.x)
        variable_y = mini_passport_rect.x + (passport_rect.y - mini_passport_rect.y)
        scaled_width = max(1,int((passport_width +12) * passport_scale))
        scaled_height = max(1, int((passport_height + 12)* passport_scale))
        scaled_passport = pygame.transform.scale(passport_surface, (scaled_width,scaled_height))
        screen.blit(scaled_passport, (int(variable_x), int(variable_y)))

    pygame.display.flip()

pygame.quit()