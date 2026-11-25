import pygame
import random
from alien import Alien
from rules import generate_rules,check_decision
from species_data import PLANET_SPECIES
from ui import PixelButton, pixel_8_bit_border, not_unbound_text

pygame.init()
LENGTH, HEIGHT = 1280,720
screen = pygame.display.set_mode((LENGTH,HEIGHT), pygame.RESIZABLE | pygame.SCALED)
pygame.display.set_caption("RuAlien?")
clock = pygame.time.Clock()
is_fullscreen = False

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

question_origin_button = PixelButton(300,500,215,50, "[1] ORIGIN?", small_font, (70,82,105),(95,112,142),(30,36,48))
question_limbs_button = PixelButton(532, 500,215,46, "[2] LIMBS?", small_font, (70,82,105),(95,112,142),(30,36,48))
question_purpose_button = PixelButton(765, 500,215,46, "[3] PURPOSE?", small_font,(70,82,105),(95,112,142),(30,36,48))

play_button = PixelButton(490, 310, 300, 80, "PLAY", big_font, (0,200,0),(50,240,100),(0,100,32))
settings_button = PixelButton(490,415,300,80, "SETTINGS", big_font, (230,180,40),(205,205,75),(120,90,15))
quit_button = PixelButton(490,520,300,80, "QUIT", big_font,(200,0,0),(240,50,100),(100,0,32))

fullscreen_button = PixelButton(440,300,400,80, "FULLSCREEN: OFF", font, (70,82,105),(95,112,142),(30,36,48))
back_button = PixelButton(490,520,300,80, "BACK", big_font, (230,180,40), (250,205,75),(120,90,15))

retry_button = PixelButton(360,460,260,80, "PLAY AGAIN", font, (0,200,0),(50,240,100),(0,100,32))
lobby_button = PixelButton(660,460,260,80, "LOBBY", font,(230,180,40),(250,205,75),(120,90,15))

def build_alien_encounter():
    alien = Alien()
    alien.doc_type = random.choices(["PASSPORT","ID CARD", "STUDENT ID"], weights=[75,15,10])[0]
    alien.doc_id = random.randint(10000,999999)

    rule = generate_rules()["RULE"]
    planets = list(PLANET_SPECIES.keys())

    lies = random.random() < 0.25
    spoken_planet = alien.passport.planet
    purpose = random.choice(["I am just passing by","I came here to work duh","I came to visit the Datei Murla Statue"])
    spoken_limbs = alien.limbs

    if lies:
        if random.choice(["planet","limbs","purpose"]) and len(planets) > 1:
            other_planet = [p for p in planets if p != alien.passport.planet]
            spoken_planet = random.choice(other_planet)
        elif lies == "limbs":
            other_limbs = [n for n in [2,4,6,8] if n != alien.limbs]
            spoken_limbs = random.choice(other_limbs)
        else:
            purpose = "STEALING... uh, TOURISM!"

    dialogue = {
        "origin": f"I traveled from {spoken_planet}.",
        "limbs": f"I have {spoken_limbs} limbs, officer.",
        "purpose": f"{purpose}",
        "is_lying": lies,
    }
    return alien, rule, dialogue
#juicy animations
animation_state = "ENTERING"
alien_y = 600.0
doc_x, doc_y = 640.0,390.0
doc_angle = 0.0
doc_target_angle = 0.0
doc_visible = False

stamp_timer = 0.0
stamp_decision = True
stamped_ink = None
shake_timer = 0.0

def start_turn_animation():
    global animation_state, alien_y,doc_x,doc_y,doc_angle,doc_target_angle,doc_visible,stamp_timer,stamped_ink
    animation_state = "ENTERING"
    alien_y = 600.0
    doc_x, doc_y = 640.0,390.0
    doc_angle = 0.0
    doc_target_angle = random.uniform(-16.0,16.0)
    doc_visible = False
    stamp_timer = 0.0
    stamped_ink = None


def reset_game():
    alien,rule,dialogue = build_alien_encounter()
    return alien,rule,dialogue, 0, 0, "", "white",0.0,""

def load_or_fallback(path,size,draw_fn):
    
#game state 
game_state = "LOBBY"
current_alien, current_rule, alien_dialogue, score, strikes, feedback_text,feedback_colour, feedback_timer, active_reply = reset_game()

#state of the game
#current_alien = Alien()
#current_rule = generate_rules()["RULE"]
#score = 0
#strikes = 0
#feedback_text = ""
#feedback_colour = "white"
#feedback_timer = 0.0

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
    mouse_pressed_true = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #lobby eveniments
        if game_state == "LOBBY":
            if play_button.clicking(event):
                current_alien, current_rule, alien_dialogue, score, strikes, feedback_text,feedback_colour, feedback_timer, active_reply = reset_game()
                passport_is_opened = False
                rules_is_opened = False
                game_state = "PLAYING"
            elif settings_button.clicking(event):
                game_state = "SETTINGS"
            elif quit_button.clicking(event):
                running = False

        #settings eveniments
        elif game_state == "SETTINGS":
            if fullscreen_button.clicking(event):
                is_fullscreen = not is_fullscreen
                if is_fullscreen:
                    screen = pygame.display.set_mode((LENGTH,HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
                else:
                    screen = pygame.display.set_mode((LENGTH, HEIGHT), pygame.RESIZABLE | pygame.SCALED)
                fullscreen_button.text = f"FULLSCREEN : {'ON'if is_fullscreen else 'OFF'}"
            elif back_button.clicking(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                game_state = "LOBBY"

        #game over eveniments(damn bro)
        elif game_state == "GAME_OVER":
            if retry_button.clicking(event):
                current_alien, current_rule, alien_dialogue, score, strikes, feedback_text,feedback_colour, feedback_timer, active_reply = reset_game()
                passport_is_opened = False
                rules_is_opened = False
                game_state = "PLAYING"
            elif lobby_button.clicking(event):
                game_state = "LOBBY"

        #playing eveniments(yayy)
        elif game_state == "PLAYING":
            if animation_state == "ENTERING":
                alien_y += (275.0-alien_y) * 9.0 * dt
                if abs (alien_y- 275.0) < 2.0:
                    alien_y = 275.0
                    animation_state = "TOSSING"
                    doc_visible = "True"
            elif animation_state == "TOSSING":
                doc_x += (185.0 - doc_x) * 8.5 * dt
                doc_y += (585.0 - doc_y) * 8.5 * dt
                doc_angle += 900 * dt
                if abs(doc_x - 185.0) < 3.0 and abs(doc_y - 585.0) < 3.0:
                    doc_x,doc_y = 185.0,585.0
                    doc_angle = doc_target_angle
                    animation_state = "WAITING"
            elif animation_state =="STAMPING":
                stamp_timer += dt
                if stamp_timer >= 0.22 and stamped_ink is None:
                    stamped_ink = "APPROVED" if stamp_decision else "DENIED"
                    shake_timer = 0.14
                if stamp_timer > 0.75:
                    valid_doc = (current_alien.doc_type == "PASSPORT")
                    real_valid = valid_doc and check_decision(current_alien,current_rule,True) and not alien_dialogue["is_lying"]
                    is_correct =(stamp_decision == real_valid)

                    if is_correct:
                        score += 1
                        feedback_text = "correct decision bro +1 matei's"
                        feedback_colour = (80,240,120)
                    else:
                        strikes += 1
                        if not valid_doc:
                            feedback_text = f"wrong bro, that was a f*#$@ing {current_alien.doc_type}"
                        else:
                            feedback_text = "wrong decision bro, you suck"
                        feedback_colour = (240, 70,90)
                    feedback_timer = 1.8
                    passport_is_opened = False
                    dragging_passport = False

                    if strikes > 3:
                        game_state = "GAME OVER"
                    else:
                        current_alien,current_rule, alien_dialogue = build_alien_encounter()
                        active_reply = ""
                        start_turn_animation()
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

                if event.key == pygame.K_SPACE:
                    current_alien = Alien()
                    current_rule = generate_rules()["RULE"]
                    passport_is_opened = False
                    dragging_passport = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                if passport_is_opened and passport_scale > 0.9:
                    close_button_rect = pygame.Rect(passport_rect.right - 45, passport_rect.y + 10,34,34)
                    title_bar_rect = pygame.Rect(passport_rect.x, passport_rect.y, passport_width - 50, 54)

                    if close_button_rect.collidepoint(event.pos):
                        passport_is_opened = False
                        dragging_passport = False
                    elif title_bar_rect.collidepoint(event.pos):
                        dragging_passport = True
                        drag_offset = (passport_rect.x - event.pos[0],passport_rect.y - event.pos[1])
                elif rules_icon_rect.collidepoint(event.pos):
                    rules_is_opened = not rules_is_opened
                elif mini_passport_rect.collidepoint(event.pos):
                    passport_is_opened = not passport_is_opened
                    dragging_passport = False

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging_passport = False

            if event.type == pygame.MOUSEMOTION and dragging_passport:
                passport_rect.x = event.pos[0] + drag_offset[0]
                passport_rect.y = event.pos[1] + drag_offset[1]
                passport_rect.clamp_ip(pygame.Rect(0,0, LENGTH, HEIGHT))

            #question buttons(question time hehe)
            clicking_on_passport = passport_is_opened and passport_rect.collidepoint(mouse_pos) if event.type == pygame.MOUSEBUTTONDOWN else False
            if animation_state == "WAITING" and not clicking_on_passport:
                if question_origin_button.clicking(event):
                    active_reply = alien_dialogue["origin"]
                if question_limbs_button.clicking(event):
                    active_reply = alien_dialogue["limbs"]
                if question_purpose_button.clicking(event):
                    active_reply = alien_dialogue["purpose"]

                #checking da decision on approve or deny
                if approve_button.clicking(event) or deny_button.clicking(event):
                    player_approval = approve_button.clicking(event)
                    stamp_decision = approve_button.clicking(event)
                    animation_state = "STAMPING"
                    dragging_passport = False

                    real_valid = check_decision(current_alien, current_rule, True) and not alien_dialogue["is_lying"]
                    is_correct = (player_approval == real_valid)

                    if is_correct:
                        score += 1
                        feedback_text = "APPROVED / DENIED CORRECTLY! +1(nice job bro)"
                        feedback_colour = (80,240,120)
                    else:
                        strikes += 1
                        feedback_text = "WRONG DECISION! (dumbass)"
                        feedback_colour = (240,70,90)

                    feedback_timer = 1.6
                    passport_is_opened = False
                    dragging_passport = False

                    if strikes >= 3:
                        game_state = "GAME_OVER"
                    else:
                        current_alien, current_rule,alien_dialogue = build_alien_encounter()
                        active_reply = ""

    #BACKGROUND
    screen.fill((58,68,88))

    if game_state == "LOBBY":
        lobby_card = pygame.Rect(340,70,600,580)
        pixel_8_bit_border(screen, lobby_card.move(10,10),(15,18,26), (15,18,26), notch = 8, border = 8)
        pixel_8_bit_border(screen,lobby_card, (34,40,54), (240,200,50), notch = 8,border = 8)

        title_surf = big_font.render("RuAlien?", True, (240,210,60))
        screen.blit(title_surf, title_surf.get_rect(centerx = 640, y =110))

        subtitle_surf = small_font.render("GALACTIC BORDER CONTROL", True, (180,190,210))
        screen.blit(subtitle_surf, subtitle_surf.get_rect(centerx = 640, y = 185))

        mini_lobby_preview_alien = pygame . transform.scale(alien_img, (84,84))
        screen.blit (mini_lobby_preview_alien, mini_lobby_preview_alien.get_rect(centerx = 640, y = 215))

        play_button.draw(screen,mouse_pos,mouse_pressed_true)
        settings_button.draw(screen,mouse_pos,mouse_pressed_true)
        quit_button.draw(screen,mouse_pos,mouse_pressed_true)

    elif game_state == "SETTINGS":
        settings_card = pygame.Rect(320,90,640,540)
        pixel_8_bit_border(screen, settings_card.move(10,10),(15,18,26), (15,18,26), notch = 8, border = 8)
        pixel_8_bit_border(screen,settings_card,(34,40,54), (240,200,50),notch = 8,border = 8)

        settings_title = big_font.render("SETTINGS & CONTROLS", True, (240,210,60))
        screen.blit(settings_title, settings_title.get_rect(centerx =650, y = 130))

        controls_lines = [
            "[P] Open / Close Passport  |  [R] Open / Close Rules",
            "[1] [2] [3] Ask Alien Questions  |  [ESC] Close Windows",
        ]
        for x, line in enumerate(controls_lines):
            controls_surface = small_font.render(line, True, (210,215,225))
            screen.blit(controls_surface, controls_surface.get_rect(centerx = 640, y=210 + x * 30))

        fullscreen_button.draw(screen, mouse_pos, mouse_pressed_true)
        back_button.draw(screen, mouse_pos, mouse_pressed_true)

    elif game_state == "PLAYING":

        #centeh window
        booth_rect = pygame.Rect(415,35,450,425)
        pixel_8_bit_border(screen, booth_rect, (28,34,46), (35,42,56), notch = 8, border = 8)
        pygame.draw.line(screen, (42,50,66), (450,70), (520,140), 4)
        pygame.draw.line(screen, (42,50,66), (475,70), (535,130), 2)

        alien_booth_rect = big_alien_image.get_rect(center=(640,int(alien_y)))
        screen.blit(big_alien_image,alien_booth_rect)

        #bubble dialogues
        if active_reply:
            bubble_rect = pygame.Rect(440,55,400,68)
            pixel_8_bit_border(screen, bubble_rect, (235,238,245), (240,200,50),notch=4, border=4)
            reply_surface = small_font.render(active_reply, True, "black")
            screen.blit(reply_surface, reply_surface.get_rect(center = bubble_rect.center))

        #table
        pygame.draw.rect(screen, (42,48,62), (0,460,1280,260))
        pygame.draw.rect(screen, (80,90,110), (0,460,1280,16))
        pygame.draw.line(screen, (20,24,32), (0,476), (1280,476), 4)
        for bolts in range(40,1280,160):
            pygame.draw.rect(screen, (35,40,45),(bolts, 465,6,6))

        #passport on the table
        active_cover = DOC_COVERS[current_alien.doc_type]
        if doc_visible:
            rotated_doc = pygame.transform.rotate(active_cover, doc_angle)
            mini_passport_rect = rotated_doc.get_rect(center = (int(doc_x), int(doc_y)))
            hovering = -5 if mini_passport_rect.collidepoint(mouse_pos) else 0
            screen.blit(cover_image, (mini_passport_rect.x, mini_passport_rect.y + hovering))

        #approve/deny buttohs
        question_origin_button.draw(screen,mouse_pos,mouse_pressed_true)
        question_limbs_button.draw(screen,mouse_pos,mouse_pressed_true)
        question_purpose_button.draw(screen,mouse_pos,mouse_pressed_true)
        
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
            rules_surface = pygame.Surface((RULES_WIDTH + 15, RULES_HEIGHT + 15 + TRANSPARENT_BORDER), pygame.SRCALPHA)
                
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
            not_unbound_text(
                rules_surface,
                f"RULE 2: Ask questions! Deny if anythin is mischevious.(bad aliens aren't allowed)!",
                rule_font,
                "black",
                pygame.Rect(0,0,RULES_WIDTH, RULES_HEIGHT),
                195,
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
            passport_surface.blit(title_text, (95,10))

            mini_photo = pygame.transform.scale(alien_img, (96,96))
            passport_surface.blit(mini_photo, (22,68))

            passport_surface.blit(small_font.render("CLASS : TRANSIT", True, (30,34,42)), (270,66))
            passport_surface.blit(small_font.render("DOCUMENT ID: #13565", True, (30,34,42)), (270,86))
            passport_surface.blit(small_font.render("SECTOR: OUTER", True, (30,34,42)), (270,106))

            passport_surface.blit(field_font.render(f"NAME: {current_alien.passport.name}",True,"black"), (165,145))
            passport_surface.blit(field_font.render(f"PLANET: {current_alien.passport.planet}", True, "black"), (165,175))
            passport_surface.blit(field_font.render(f"EXPIRES : {current_alien.passport.expiration_date}", True, "black"), (165,205))
            passport_surface.blit(field_font.render(f"LIMBS : {current_alien.passport.limbs}",True, "black"), (165, 235))

            bars = 260
            for width in [3,3,2,2,4,2,4,6,3,4,5,3,2,2,2,3,4,4,2,2,3,5,2]:
                pygame.draw.rect(passport_surface, "black", (bars, 265, width, 36))
                bars += width + 4

            x_button_close_rect = pygame.Rect(passport_width - 45 , 10, 25, 25)
            global_close_button = x_button_close_rect.move(passport_rect.x, passport_rect.y)

            x_button_background = (240,60,80) if global_close_button.collidepoint(mouse_pos) else (185,30,40)
            pygame.draw.rect(passport_surface, x_button_background, x_button_close_rect,0,8)
            pygame.draw.rect(passport_surface, (255,255,255), x_button_close_rect,2,8)
            x_button_close_text = small_font.render("X", True, "white")
            passport_surface.blit(x_button_close_text, x_button_close_text.get_rect(center =x_button_close_rect.center))

            variable_x = mini_passport_rect.x + (passport_rect.x - mini_passport_rect.x) * passport_scale
            variable_y = mini_passport_rect.y + (passport_rect.y - mini_passport_rect.y) * passport_scale
            scaled_width = max(1,int((passport_width +12) * passport_scale))
            scaled_height = max(1, int((passport_height + 12)* passport_scale))
            scaled_passport = pygame.transform.scale(passport_surface, (scaled_width,scaled_height))
            screen.blit(scaled_passport, (int(variable_x), int(variable_y)))

    elif game_state == "GAME_OVER":
        game_over_card = pygame.Rect(310,130,660,460)
        pixel_8_bit_border(screen, game_over_card.move(10,10), (15,18,26), (15,18,26), notch = 8, border = 8)
        pixel_8_bit_border(screen, game_over_card, (34,40,54), (220,45,65), notch = 8, border = 8)

        game_over_title = big_font.render("GAME OVER", True,(200,205,215))
        screen.blit(game_over_title, game_over_title.get_rect(centerx = 640, y = 185))

        reason_surface = rule_font.render("3 STRIKES REACHED - you suck, everybody died bcus of you)", True,(200,205,215))
        screen.blit(reason_surface, reason_surface.get_rect(centerx = 640, y = 265))

        final_score_surface = big_font.render(f"FINAL SCORE: {score}", True, (240,210,60))
        screen.blit(final_score_surface, final_score_surface.get_rect(centerx = 640, y = 335))

        retry_button.draw(screen,mouse_pos,mouse_pressed_true)
        lobby_button.draw(screen,mouse_pos,mouse_pressed_true)

    pygame.display.flip()

pygame.quit()