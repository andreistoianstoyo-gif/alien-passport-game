import pygame
import random
import math
import asyncio
import sys
from alien import Alien
from rules import generate_rules, evaluate_encounter
from species_data import PLANETS_SPECIES
from ui import PixelButton, pixel_8_bit_border, not_unbound_text
from alien_renderer import render_species_preview, render_alien_sprite

pygame.init()
LENGTH, HEIGHT = 1280, 720
if sys.platform == "emscripten":
    screen = pygame.display.set_mode((LENGTH, HEIGHT))
else: 
    screen = pygame.display.set_mode((LENGTH, HEIGHT), pygame.RESIZABLE | pygame.SCALED)
pygame.display.set_caption("RuAlien?")
clock = pygame.time.Clock()
is_fullscreen = False

# the fonts duh
font = pygame.font.Font("assets/fonts/PixelifySans-Regular.ttf", 28)
big_font = pygame.font.Font("assets/fonts/PixelifySans-Regular.ttf", 40)
rule_font = pygame.font.Font("assets/fonts/PixelifySans-Regular.ttf", 24)
small_font = pygame.font.Font("assets/fonts/PixelifySans-Regular.ttf", 18)
field_font = pygame.font.Font("assets/fonts/PixelifySans-Regular.ttf", 16)
passport_font = pygame.font.Font("assets/fonts/PixelifySans-Regular.ttf", 14)

# da sprites
raw_passport = pygame.image.load("assets/sprites/passport.png").convert_alpha()
passport_image = pygame.transform.scale_by(raw_passport, 3)
passport_shadow_image = pygame.mask.from_surface(passport_image).to_surface(
    setcolor=(10, 12, 18, 255), unsetcolor=(0, 0, 0, 0)
)

passport_width, passport_height = passport_image.get_size()
passport_rect = pygame.Rect(35, 68, passport_width, passport_height)

try:
    raw_cover = pygame.image.load("assets/sprites/passport_cover.png").convert_alpha()
    cover_image = pygame.transform.scale_by(raw_cover, 3)
except FileNotFoundError:
    cover_image = pygame.Surface((108, 144), pygame.SRCALPHA)
    pixel_8_bit_border(cover_image, pygame.Rect(0, 0, 108, 144), (32, 45, 75), (20, 28, 48), notch=4, border=4)
    pygame.draw.rect(cover_image, (240, 200, 50), (36, 42, 36, 36), 4)

mini_passport_rect = cover_image.get_rect(topleft=(140, 515))

rules_icon = pygame.image.load("assets/sprites/rules.png").convert_alpha()
rules_icon = pygame.transform.scale(rules_icon, (192, 192))
rules_icon_rect = rules_icon.get_rect(topright=(1305, 0))


def load_or_fallback(path, size, draw_fn):
    try:
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, size)
    except FileNotFoundError:
        surface = pygame.Surface(size, pygame.SRCALPHA)
        draw_fn(surface)
        return surface


# covers for the wrong type of documentation
def _draw_id_card_fallback(surface):
    pixel_8_bit_border(surface, pygame.Rect(0, 0, 144, 96), (55, 115, 175), (25, 45, 80), notch=4, border=4)
    pygame.draw.rect(surface, (240, 210, 60), (16, 22, 34, 44), 2)
    pygame.draw.line(surface, (230, 235, 245), (62, 30), (126, 30), 3)
    pygame.draw.line(surface, (230, 235, 245), (62, 48), (114, 48), 3)


def _draw_student_fallback(surface):
    pixel_8_bit_border(surface, pygame.Rect(0, 0, 108, 144), (165, 48, 62), (75, 20, 28), notch=4, border=4)
    pygame.draw.circle(surface, (240, 210, 60), (54, 58), 18, 3)
    pygame.draw.line(surface, (240, 230, 220), (24, 98), (84, 98), 3)


def _draw_stamp_fallback(surface):
    pygame.draw.rect(surface, (130, 75, 40), (22, 0, 28, 46), border_radius=8)
    pygame.draw.rect(surface, (45, 50, 62), (6, 42, 60, 24), border_radius=4)
    pygame.draw.rect(surface, (200, 50, 60), (10, 60, 52, 8))


def _draw_bestiary_icon_fallback(surface):
    pixel_8_bit_border(surface, pygame.Rect(10, 8, 86, 104), (92, 46, 125), (38, 18, 56), notch=4, border=4)
    pygame.draw.rect(surface, (55, 24, 80), (10, 8, 14, 104))
    pygame.draw.rect(surface, (240, 200, 50), (34, 24, 44, 34), 3)
    pygame.draw.circle(surface, (120, 235, 140), (56, 41), 9)
    label = passport_font.render("[B] DEX", True, (240, 210, 60))
    surface.blit(label, label.get_rect(center=(56, 84)))


def _make_ink_stamp(text, colour):
    surface = pygame.Surface((170, 54), pygame.SRCALPHA)
    pygame.draw.rect(surface, colour, (2, 2, 166, 50), 4, border_radius=4)
    rendered = font.render(text, True, colour)
    surface.blit(rendered, rendered.get_rect(center=(85, 27)))
    return pygame.transform.rotate(surface, -12)


id_card_cover_image = load_or_fallback("assets/sprites/id_card.png", (144, 96), _draw_id_card_fallback)
id_card_cover_open = pygame.transform.scale_by(id_card_cover_image, 3)
id_card_cover_shadow = pygame.mask.from_surface(id_card_cover_open).to_surface(
    setcolor=(10, 12, 18, 255), unsetcolor=(0, 0, 0, 0)
)
student_id_cover_image = load_or_fallback("assets/sprites/student_id_cover.png", (108, 144), _draw_student_fallback)
stamp_tool_image = load_or_fallback("assets/sprites/stamp_tool.png", (72, 74), _draw_stamp_fallback)
bestiary_icon = load_or_fallback("assets/sprites/bestiary.png", (106, 120), _draw_bestiary_icon_fallback)
bestiary_icon_rect = bestiary_icon.get_rect(topright=(1258, 195))

ink_approved_image = _make_ink_stamp("APPROVED", (30, 175, 70))
ink_denied_image = _make_ink_stamp("DENIED", (215, 70, 55))

DOC_COVERS = {
    "PASSPORT": cover_image,
    "ID CARD": id_card_cover_image,
    "STUDENT ID": student_id_cover_image,
}

SPECIES_PREVIEWS = {
    planet: render_species_preview(planet, (68, 68))
    for planet in PLANETS_SPECIES
}

# buttuhs
approve_button = PixelButton(300, 605, 270, 90, "APPROVE", big_font, (0, 200, 0), (50, 240, 100), (0, 100, 32))
deny_button = PixelButton(700, 605, 280, 90, "DENY", big_font, (200, 0, 0), (240, 50, 100), (100, 0, 32))

question_origin_button = PixelButton(300, 500, 215, 50, "[1] ORIGIN?", small_font, (70, 82, 105), (95, 112, 142), (30, 36, 48))
question_limbs_button = PixelButton(532, 500, 215, 50, "[2] LIMBS?", small_font, (70, 82, 105), (95, 112, 142), (30, 36, 48))
question_purpose_button = PixelButton(765, 500, 215, 50, "[3] PURPOSE?", small_font, (70, 82, 105), (95, 112, 142), (30, 36, 48))

bestiary_previous_button = PixelButton(935, 455, 65, 38, "<", small_font, (125, 75, 165), (155, 95, 200), (45, 22, 65))
bestiary_next_button = PixelButton(1165, 455, 65, 38, ">", small_font, (125, 75, 165), (155, 95, 200), (45, 22, 65))

play_button = PixelButton(490, 310, 300, 80, "PLAY", big_font, (0, 200, 0), (50, 240, 100), (0, 100, 32))
settings_button = PixelButton(490, 415, 300, 80, "SETTINGS", big_font, (230, 180, 40), (205, 205, 75), (120, 90, 15))
quit_button = PixelButton(490, 520, 300, 80, "QUIT", big_font, (200, 0, 0), (240, 50, 100), (100, 0, 32))

fullscreen_button = PixelButton(440, 300, 400, 80, "FULLSCREEN: OFF", font, (70, 82, 105), (95, 112, 142), (30, 36, 48))
back_button = PixelButton(490, 520, 300, 80, "BACK", big_font, (230, 180, 40), (250, 205, 75), (120, 90, 15))

retry_button = PixelButton(360, 460, 260, 80, "PLAY AGAIN", font, (0, 200, 0), (50, 240, 100), (0, 100, 32))
lobby_button = PixelButton(660, 460, 260, 80, "LOBBY", font, (230, 180, 40), (250, 205, 75), (120, 90, 15))


def build_alien_encounter():
    alien = Alien()
    alien.booth_sprite = render_alien_sprite(alien, (256, 256))
    alien.photo_sprite = render_alien_sprite(alien, (96, 96))

    planets = list(PLANETS_SPECIES.keys())

    lies = random.random() < 0.25
    spoken_planet = alien.passport.planet
    purpose = random.choice(["I am just passing by", "I came here to work duh", "I came to visit the Datei Murla Statue"])
    spoken_limbs = alien.limbs

    if lies:
        lie_type = random.choice(["planet", "limbs", "purpose"])
        if lie_type == "planet" and len(planets) > 1:
            other_planet = [p for p in planets if p != alien.passport.planet]
            spoken_planet = random.choice(other_planet)
        elif lie_type == "limbs":
            other_limbs = [n for n in [2, 4, 6, 8] if n != alien.limbs]
            spoken_limbs = random.choice(other_limbs)
        else:
            purpose = "to snatch some shi"

    dialogue = {
        "origin": f"I traveled from {spoken_planet}.",
        "limbs": f"I have {spoken_limbs} limbs, officer.",
        "purpose": f"{purpose}",
        "is_lying": lies,
    }
    return alien, dialogue


# juicy animations
animation_state = "ENTERING"
alien_x = 960.0
doc_x, doc_y = 640.0, 430.0
doc_angle = -45.0
doc_target_angle = 0.0
doc_t = 0.0
doc_visible = False

stamp_timer = 0.0
stamp_decision = True
stamped_ink = None
shake_timer = 0.0


def start_turn_animation():
    global animation_state, alien_x, doc_x, doc_y, doc_angle, doc_target_angle, doc_t, doc_visible, stamp_timer, stamped_ink
    animation_state = "ENTERING"
    alien_x = 960.0
    doc_x, doc_y = 640.0, 390.0
    doc_angle = -45.0
    doc_target_angle = random.uniform(-14.0, 14.0)
    doc_t = 0
    doc_visible = False
    stamp_timer = 0.0
    stamped_ink = None


def reset_game():
    global day, aliens_today, game_over_reason, bestiary_page
    alien, dialogue = build_alien_encounter()
    rule = generate_rules()["RULE"]
    start_turn_animation()
    day = 1
    aliens_today = 0
    bestiary_page = 0
    game_over_reason = ""
    return alien, rule, dialogue, 0, 0, "", "white", 0.0, ""


# game state
game_state = "LOBBY"
day = 1
aliens_today = 0
game_over_reason = ""
bestiary_page = 0
SPECIES_PER_PAGE = 2
current_alien, current_rule, alien_dialogue, score, strikes, feedback_text, feedback_colour, feedback_timer, active_reply = reset_game()
lobby_preview_alien = current_alien.photo_sprite

# ui windows settings
passport_is_opened = False
passport_scale = 0.0
dragging_passport = False
drag_offset = (0, 0)

rules_is_opened = False
rules_scale = 0.0

bestiary_is_open = False
bestiary_scale = 0.0

async def main():
    global is_fullscreen,screen,game_state,running
    global current_alien, current_rule, alien_dialogue, score, strikes
    global feedback_text, feedback_colour, feedback_timer, active_reply
    global passport_is_opened, passport_scale, feedback_timer, active_reply
    global rules_is_opened, rules_scale, bestiary_is_open, bestiary_scale, bestiary_page
    global animation_state, alien_x, doc_x,doc_y, doc_angle, doc_t, doc_visible
    global stamp_timer,stamp_decision, stamped_ink, shake_timer
    global day,aliens_today, game_over_reason, mini_passport_rect

    running = True
    while running:
        target_fps = 30 if sys.platform == "emscripten" else 60
        dt = clock.tick(60) / 1000
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed_true = pygame.mouse.get_pressed()

        species_items = list(PLANETS_SPECIES.items())
        total_bestiary_pages = max(1, math.ceil(len(species_items) / SPECIES_PER_PAGE))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # lobby eveniments
            if game_state == "LOBBY":
                if play_button.clicking(event):
                    current_alien, current_rule, alien_dialogue, score, strikes, feedback_text, feedback_colour, feedback_timer, active_reply = reset_game()
                    passport_is_opened = False
                    rules_is_opened = True
                    bestiary_is_open = False
                    game_state = "PLAYING"
                elif settings_button.clicking(event):
                    game_state = "SETTINGS"
                elif quit_button.clicking(event):
                    running = False

            # settings eveniments
            elif game_state == "SETTINGS":
                if fullscreen_button.clicking(event):
                    is_fullscreen = not is_fullscreen
                    if is_fullscreen:
                        screen = pygame.display.set_mode((LENGTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
                    else:
                        screen = pygame.display.set_mode((LENGTH, HEIGHT), pygame.RESIZABLE | pygame.SCALED)
                    fullscreen_button.text = f"FULLSCREEN: {'ON' if is_fullscreen else 'OFF'}"
                elif back_button.clicking(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    game_state = "LOBBY"

            # game over eveniments(damn bro)
            elif game_state == "GAME OVER":
                if retry_button.clicking(event):
                    current_alien, current_rule, alien_dialogue, score, strikes, feedback_text, feedback_colour, feedback_timer, active_reply = reset_game()
                    passport_is_opened = False
                    rules_is_opened = True
                    bestiary_is_open = False
                    game_state = "PLAYING"
                elif lobby_button.clicking(event):
                    game_state = "LOBBY"

            # playing eveniments(yayy)
            elif game_state == "PLAYING":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        rules_is_opened = not rules_is_opened
                        if rules_is_opened:
                            bestiary_is_open = False

                    if event.key == pygame.K_b:
                        bestiary_is_open = not bestiary_is_open
                        if bestiary_is_open:
                            rules_is_opened = False

                    if bestiary_is_open:
                        if event.key == pygame.K_LEFT:
                            bestiary_page = (bestiary_page - 1) % total_bestiary_pages
                        elif event.key == pygame.K_RIGHT:
                            bestiary_page = (bestiary_page + 1) % total_bestiary_pages

                    if event.key == pygame.K_p and doc_visible:
                        passport_is_opened = not passport_is_opened
                        dragging_passport = False

                    if event.key == pygame.K_ESCAPE:
                        passport_is_opened = False
                        rules_is_opened = False
                        bestiary_is_open = False
                        dragging_passport = False

                    if animation_state == "WAITING":
                        if event.key == pygame.K_1:
                            active_reply = alien_dialogue["origin"]
                        if event.key == pygame.K_2:
                            active_reply = alien_dialogue["limbs"]
                        if event.key == pygame.K_3:
                            active_reply = alien_dialogue["purpose"]

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    click_absorbed = False

                    if passport_is_opened and passport_scale > 0.9 and passport_rect.collidepoint(event.pos):
                        click_absorbed = True
                        close_button_rect = pygame.Rect(passport_rect.right - 45, passport_rect.y + 10, 34, 34)
                        title_bar_rect = pygame.Rect(passport_rect.x, passport_rect.y, passport_rect.width - 50, 54)

                        if close_button_rect.collidepoint(event.pos):
                            passport_is_opened = False
                            dragging_passport = False
                        elif title_bar_rect.collidepoint(event.pos):
                            dragging_passport = True
                            drag_offset = (passport_rect.x - event.pos[0], passport_rect.y - event.pos[1])
                    if not click_absorbed and bestiary_is_open and bestiary_scale > 0.9:
                        if bestiary_previous_button.clicking(event):
                            bestiary_page = (bestiary_page - 1) % total_bestiary_pages
                            click_absorbed = True
                        elif bestiary_next_button.clicking(event):
                            bestiary_page = (bestiary_page + 1) % total_bestiary_pages
                            click_absorbed = True

                    if not click_absorbed:
                        if rules_icon_rect.collidepoint(event.pos):
                            rules_is_opened = not rules_is_opened
                            if rules_is_opened:
                                bestiary_is_open = False
                            click_absorbed = True
                        elif bestiary_icon_rect.collidepoint(event.pos):
                            bestiary_is_open = not bestiary_is_open
                            if bestiary_is_open:
                                rules_is_opened = False
                            click_absorbed = True
                        elif doc_visible and mini_passport_rect.collidepoint(event.pos):
                            passport_is_opened = not passport_is_opened
                            dragging_passport = False
                            click_absorbed = True


                    if not click_absorbed and animation_state == "WAITING":
                        if question_origin_button.clicking(event):
                            active_reply = alien_dialogue["origin"]
                        elif question_limbs_button.clicking(event):
                            active_reply = alien_dialogue["limbs"]
                        elif question_purpose_button.clicking(event):
                            active_reply = alien_dialogue["purpose"]
                        elif approve_button.clicking(event):
                            stamp_decision = True
                            animation_state = "STAMPING"
                            stamp_timer = 0.0
                            dragging_passport = False
                        elif deny_button.clicking(event):
                            stamp_decision = False
                            animation_state = "STAMPING"
                            stamp_timer = 0.0
                            dragging_passport = False

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    dragging_passport = False

                if event.type == pygame.MOUSEMOTION and dragging_passport:
                    passport_rect.x = event.pos[0] + drag_offset[0]
                    passport_rect.y = event.pos[1] + drag_offset[1]
                    passport_rect.clamp_ip(pygame.Rect(0, 0, LENGTH, HEIGHT))

        # BACKGROUND
        screen.fill((58, 68, 88))

        if game_state == "LOBBY":
            lobby_card = pygame.Rect(340, 70, 600, 580)
            pixel_8_bit_border(screen, lobby_card.move(10, 10), (15, 18, 26), (15, 18, 26), notch=8, border=8)
            pixel_8_bit_border(screen, lobby_card, (34, 40, 54), (240, 200, 50), notch=8, border=8)

            title_surf = big_font.render("RuAlien?", True, (240, 210, 60))
            screen.blit(title_surf, title_surf.get_rect(centerx=640, y=110))

            subtitle_surf = small_font.render("GALACTIC BORDER CONTROL", True, (180, 190, 210))
            screen.blit(subtitle_surf, subtitle_surf.get_rect(centerx=640, y=185))

            mini_lobby_preview_alien = pygame.transform.scale(lobby_preview_alien, (84, 84))
            screen.blit(mini_lobby_preview_alien, mini_lobby_preview_alien.get_rect(centerx=640, y=215))

            play_button.draw(screen, mouse_pos, mouse_pressed_true)
            settings_button.draw(screen, mouse_pos, mouse_pressed_true)
            quit_button.draw(screen, mouse_pos, mouse_pressed_true)

        elif game_state == "SETTINGS":
            settings_card = pygame.Rect(320, 90, 640, 540)
            pixel_8_bit_border(screen, settings_card.move(10, 10), (15, 18, 26), (15, 18, 26), notch=8, border=8)
            pixel_8_bit_border(screen, settings_card, (34, 40, 54), (240, 200, 50), notch=8, border=8)

            settings_title = big_font.render("SETTINGS & CONTROLS", True, (240, 210, 60))
            screen.blit(settings_title, settings_title.get_rect(centerx=650, y=130))

            controls_lines = [
                "[P] Open / Close Passport  |  [R] Rules  |  [B] Bestiary",
                "[1] [2] [3] Ask Alien Questions  |  [ESC] Close Windows",
            ]
            for x, line in enumerate(controls_lines):
                controls_surface = small_font.render(line, True, (210, 215, 225))
                screen.blit(controls_surface, controls_surface.get_rect(centerx=640, y=210 + x * 30))

            fullscreen_button.draw(screen, mouse_pos, mouse_pressed_true)
            back_button.draw(screen, mouse_pos, mouse_pressed_true)

        elif game_state == "PLAYING":
            if animation_state == "ENTERING":
                alien_x += (640.0 - alien_x) * 8.0 * dt
                if abs(alien_x - 640.0) < 2.0:
                    alien_x = 640.0
                    animation_state = "TOSSING"
                    doc_visible = True
            elif animation_state == "TOSSING":
                doc_t = min(1.0, doc_t + dt / 0.32)
                ease = 1.0 - (1.0 - doc_t) ** 3
                doc_x = 640.0 + (185.0 - 640.0) * ease
                doc_y = 430.0 + (585.0 - 430.0) * ease
                doc_angle = -45.0 + (doc_target_angle + 45.0) * ease
                if doc_t >= 1.0:
                    animation_state = "WAITING"
            elif animation_state == "STAMPING":
                stamp_timer += dt
                if stamp_timer >= 0.22 and stamped_ink is None:
                    stamped_ink = "APPROVED" if stamp_decision else "DENIED"
                    shake_timer = 0.14
                if stamp_timer > 0.75:
                    real_valid, fail_reason = evaluate_encounter(current_alien, current_rule, alien_dialogue)
                    is_correct = (stamp_decision == real_valid)

                    if is_correct:
                        score += 1
                        feedback_text = "correct decision bro"
                        feedback_colour = (80, 240, 120)
                    else:
                        strikes += 1
                        feedback_text = fail_reason if fail_reason else "Wrong! That alien was actually valid!"
                        feedback_colour = (240, 70, 90)

                    aliens_today += 1
                    if aliens_today >= 5:
                        day += 1
                        aliens_today = 0
                        current_rule = generate_rules()["RULE"]
                        rules_is_opened = True
                        bestiary_is_open = False
                        feedback_text = f"Day {day} has started! Check new rule!"
                        feedback_colour = (240, 210, 60)

                    feedback_timer = 2.2
                    passport_is_opened = False
                    dragging_passport = False

                    if strikes >= 3:
                        game_over_reason = "3 STRIKES REACHED - you suck, everybody died bcus of you"
                        game_state = "GAME OVER"
                    elif day >= 8:
                        game_over_reason = "SHIFT COMPLETE! YOU SURVIVED ALL 7 DAYS!"
                        game_state = "GAME OVER"
                    else:
                        current_alien, alien_dialogue = build_alien_encounter()
                        active_reply = ""
                        start_turn_animation()

            # centeh window
            booth_rect = pygame.Rect(415, 35, 450, 425)
            pixel_8_bit_border(screen, booth_rect, (28, 34, 46), (35, 42, 56), notch=8, border=8)
            pygame.draw.line(screen, (42, 50, 66), (450, 70), (520, 140), 4)
            pygame.draw.line(screen, (42, 50, 66), (475, 70), (535, 130), 2)

            screen.set_clip(booth_rect.inflate(-16, 16))
            walk_bob = abs((alien_x - 640.0) % 44 - 22) * 0.3 if animation_state == "ENTERING" else 0
            alien_booth_rect = current_alien.booth_sprite.get_rect(center=(int(alien_x), int(275 - walk_bob)))
            screen.blit(current_alien.booth_sprite, alien_booth_rect)
            screen.set_clip(None)

            # bubble dialogues
            if active_reply:
                bubble_rect = pygame.Rect(440, 55, 400, 68)
                pixel_8_bit_border(screen, bubble_rect, (235, 238, 245), (240, 200, 50), notch=4, border=4)
                reply_surface = small_font.render(active_reply, True, "black")
                screen.blit(reply_surface, reply_surface.get_rect(center=bubble_rect.center))

            # table
            pygame.draw.rect(screen, (42, 48, 62), (0, 460, 1280, 260))
            pygame.draw.rect(screen, (80, 90, 110), (0, 460, 1280, 16))
            pygame.draw.line(screen, (20, 24, 32), (0, 476), (1280, 476), 4)
            for bolts in range(40, 1280, 160):
                pygame.draw.rect(screen, (35, 40, 45), (bolts, 465, 6, 6))

            # passport on the table
            active_cover = DOC_COVERS[current_alien.doc_type]
            if doc_visible:
                rotated_doc = pygame.transform.rotate(active_cover, doc_angle)
                mini_passport_rect = rotated_doc.get_rect(center=(int(doc_x), int(doc_y)))
                hovering = -5 if (animation_state == "WAITING" and mini_passport_rect.collidepoint(mouse_pos)) else 0
                screen.blit(rotated_doc, (mini_passport_rect.x, mini_passport_rect.y + hovering))

            # approve/deny buttohs
            question_origin_button.draw(screen, mouse_pos, mouse_pressed_true)
            question_limbs_button.draw(screen, mouse_pos, mouse_pressed_true)
            question_purpose_button.draw(screen, mouse_pos, mouse_pressed_true)

            approve_button.draw(screen, mouse_pos, mouse_pressed_true)
            deny_button.draw(screen, mouse_pos, mouse_pressed_true)

            # HUD (scores and all of that blah-blah)
            hud_text = rule_font.render(f"SCORE:{score} | STRIKES: {strikes}/3", True, "white")
            screen.blit(hud_text, (40, 40))
            days_text = rule_font.render(f"DAY:{day}", True, "white")
            screen.blit(days_text, (300, 40))

            if feedback_timer > 0:
                feedback_timer -= dt
                feedback_surface = rule_font.render(feedback_text, True, feedback_colour)
                screen.blit(feedback_surface, feedback_surface.get_rect(centerx=640, y=10))

            # daily rules & bestiary icons
            if rules_icon_rect.collidepoint(mouse_pos):
                screen.blit(rules_icon, (rules_icon_rect.x, rules_icon_rect.y - 3))
            else:
                screen.blit(rules_icon, rules_icon_rect)

            if bestiary_icon_rect.collidepoint(mouse_pos):
                screen.blit(bestiary_icon, (bestiary_icon_rect.x, bestiary_icon_rect.y - 3))
            else:
                screen.blit(bestiary_icon, bestiary_icon_rect)

            # daily rules things
            target_scale = 1.0 if rules_is_opened else 0.0
            rules_scale += (target_scale - rules_scale) * 20 * dt
            if abs(target_scale - rules_scale) < 0.01:
                rules_scale = target_scale

            if rules_scale > 0.05:
                RULES_WIDTH, RULES_HEIGHT = 290, 480
                TRANSPARENT_BORDER = 14
                rules_surface = pygame.Surface((RULES_WIDTH + 15, RULES_HEIGHT + 15 + TRANSPARENT_BORDER), pygame.SRCALPHA)

                pygame.draw.rect(rules_surface, (15, 17, 24), (15, 15 + TRANSPARENT_BORDER, RULES_WIDTH, RULES_HEIGHT), 0, 17)
                pygame.draw.rect(rules_surface, (0, 190, 230), (0, TRANSPARENT_BORDER, RULES_WIDTH, RULES_HEIGHT), 0, 17)
                pygame.draw.rect(rules_surface, (10, 75, 220), (0, TRANSPARENT_BORDER, RULES_WIDTH + 3, RULES_HEIGHT + 3), 7, 20)

                rules_title = font.render("DAILY RULES", True, "black")
                rules_title_rect = rules_title.get_rect(centerx=RULES_WIDTH // 2, y=20 + TRANSPARENT_BORDER)
                rules_surface.blit(rules_title, rules_title_rect)
                pygame.draw.line(rules_surface, (12, 17, 24), (25, 55 + TRANSPARENT_BORDER), (RULES_WIDTH - 25, 55 + TRANSPARENT_BORDER), 3)
                pygame.draw.line(rules_surface, (200, 200, 0), (100, 3 + TRANSPARENT_BORDER), (RULES_WIDTH - 100, 3 + TRANSPARENT_BORDER), 7)
                pygame.draw.line(rules_surface, (220, 220, 0), (100, TRANSPARENT_BORDER), (RULES_WIDTH - 100, TRANSPARENT_BORDER), 12)

                not_unbound_text(
                    rules_surface,
                    f"RULE 1: {current_rule}",
                    rule_font,
                    "black",
                    pygame.Rect(0, 0, RULES_WIDTH, RULES_HEIGHT),
                    75,
                )
                not_unbound_text(
                    rules_surface,
                    "RULE 2: Ask questions! Deny if anything is mischievous or doc is not passport!",
                    rule_font,
                    "black",
                    pygame.Rect(0, 0, RULES_WIDTH, RULES_HEIGHT),
                    195,
                )

                if rules_scale >= 0.99:
                    screen.blit(rules_surface, rules_surface.get_rect(topright=(1250, 30)))
                else:
                    NEW_WIDTH = max(1, int(RULES_WIDTH * rules_scale))
                    NEW_HEIGHT = max(1, int(RULES_HEIGHT * rules_scale))
                    scaled_panel = pygame.transform.scale(rules_surface, (NEW_WIDTH, NEW_HEIGHT))
                    screen.blit(scaled_panel, scaled_panel.get_rect(topright=(1250, 30)))

            # GALACTIC BESTIARY WINDOW
            target_bestiary_scale = 1.0 if bestiary_is_open else 0.0
            bestiary_scale += (target_bestiary_scale - bestiary_scale) * 20 * dt
            if abs(target_bestiary_scale - bestiary_scale) < 0.01:
                bestiary_scale = target_bestiary_scale

            if bestiary_scale > 0.05:
                BESTIARY_WIDTH, BESTIARY_HEIGHT = 330, 480
                bestiary_surface = pygame.Surface((BESTIARY_WIDTH + 14, BESTIARY_HEIGHT + 14), pygame.SRCALPHA)
                pixel_8_bit_border(bestiary_surface, pygame.Rect(10, 10, BESTIARY_WIDTH, BESTIARY_HEIGHT), (14, 16, 24), (14, 16, 24), notch=8, border=8)
                pixel_8_bit_border(bestiary_surface, pygame.Rect(0, 0, BESTIARY_WIDTH, BESTIARY_HEIGHT), (42, 28, 62), (235, 195, 55), notch=8, border=8)

                bestiary_title = rule_font.render("GALACTIC BESTIARY", True, (240, 210, 60))
                bestiary_surface.blit(bestiary_title, bestiary_title.get_rect(centerx=BESTIARY_WIDTH // 2, y=18))
                pygame.draw.line(bestiary_surface, (235, 195, 55), (20, 52), (BESTIARY_WIDTH - 20, 52), 3)

                start_idk = bestiary_page * SPECIES_PER_PAGE
                page_entries = species_items[start_idk:start_idk + SPECIES_PER_PAGE]

                for i, (planet_name, traits) in enumerate(page_entries):
                    card_y = 68 + i * 172
                    card_rect = pygame.Rect(18, card_y, BESTIARY_WIDTH - 36, 158)
                    pixel_8_bit_border(bestiary_surface, card_rect, (28, 22, 42), (125, 85, 175), notch=4, border=4)

                    preview_box = pygame.Rect(28, card_y + 20, 76, 76)
                    pygame.draw.rect(bestiary_surface, (18, 22, 32), preview_box)
                    pygame.draw.rect(bestiary_surface, (235, 195, 55), preview_box, 2)
                    bestiary_surface.blit(SPECIES_PREVIEWS[planet_name], (32, card_y + 24))

                    planet_surface = rule_font.render(planet_name.upper(), True, (240, 210, 60))
                    bestiary_surface.blit(planet_surface, (114, card_y + 14))

                    bestiary_surface.blit(
                        field_font.render(f"EYES: {traits['eyes']}", True, (230, 235, 245)),
                        (114, card_y + 48),
                    )
                    bestiary_surface.blit(
                        field_font.render(f"COLOUR: {traits['colour'].upper()}", True, (230, 235, 245)),
                        (114, card_y + 74),
                    )
                    bestiary_surface.blit(
                        field_font.render(f"LIMBS: {traits['limbs']}", True, (230, 235, 245)),
                        (114, card_y + 100),
                    )
                    bestiary_surface.blit(
                        passport_font.render(f"TRAIT: {traits.get('accessory', 'none').upper()}", True, (180, 170, 210)),
                        (28, card_y + 126),
                    )

                page_surface = small_font.render(f"PAGE {bestiary_page + 1}/{total_bestiary_pages}", True, (230, 235, 245))
                bestiary_surface.blit(page_surface, page_surface.get_rect(centerx=BESTIARY_WIDTH // 2, y=BESTIARY_HEIGHT - 44))

                scaled_bestiary_width = max(1, int((BESTIARY_WIDTH + 14) * bestiary_scale))
                scaled_bestiary_height = max(1, int((BESTIARY_HEIGHT + 14) * bestiary_scale))
                scaled_bestiary = pygame.transform.scale(bestiary_surface, (scaled_bestiary_width, scaled_bestiary_height))
                bestiary_rect = scaled_bestiary.get_rect(topright=(1250, 30))
                screen.blit(scaled_bestiary, bestiary_rect)

                if bestiary_scale > 0.9:
                    bestiary_previous_button.draw(screen, mouse_pos, mouse_pressed_true)
                    bestiary_next_button.draw(screen, mouse_pos, mouse_pressed_true)

            # PASSPORTTTTTTT
            target_idk_scale = 1.0 if passport_is_opened else 0.0
            passport_scale += (target_idk_scale - passport_scale) * 20 * dt
            if abs(target_idk_scale - passport_scale) < 0.01:
                passport_scale = target_idk_scale

            if passport_scale > 0.05:
                is_id_card = (current_alien.doc_type == "ID CARD")
                active_background = id_card_cover_open if is_id_card else passport_image
                active_shadow = id_card_cover_shadow if is_id_card else passport_shadow_image
                doc_width, doc_height = active_background.get_size()
                passport_rect.size = (doc_width, doc_height)
                passport_rect.clamp_ip(pygame.Rect(0, 0, LENGTH, HEIGHT))

                passport_surface = pygame.Surface((doc_width + 12, doc_height + 12), pygame.SRCALPHA)
                passport_surface.blit(active_shadow, (10, 10))
                passport_surface.blit(active_background, (0, 0))

                mini_photo = current_alien.photo_sprite
                if is_id_card:
                    title_text = rule_font.render("PLANETARY ID", True, (120, 200, 255))
                    passport_surface.blit(title_text, (120, 5))
                    passport_surface.blit(mini_photo, (20, 56))
                    passport_surface.blit(field_font.render(f"ID : #{current_alien.doc_id}", True, (30, 34, 42)), (240, 80))

                    passport_surface.blit(field_font.render("SECTOR: OUTER", True, (30, 34, 42)), (240, 100))
                    passport_surface.blit(field_font.render(f"NAME: {current_alien.passport.name}", True, "black"), (150, 125))
                    passport_surface.blit(field_font.render(f"PLANET: {current_alien.passport.planet}", True, "black"), (150, 155))
                    passport_surface.blit(field_font.render(f"LIMBS: {current_alien.limbs}", True, "black"), (150, 180))
                    passport_surface.blit(field_font.render("CLASS: TRANSIT | OUTER", True, (30, 34, 42)), (240, 60))

                    bars = 200
                    for width in [3, 2, 2, 4, 2, 3, 3, 2, 2, 4, 3, 3, 5, 2, 2, 2, 2, 3, 3, 4, 4, 2, 2, 3, 4]:
                        pygame.draw.rect(passport_surface, "black", (bars, doc_height - 48, width, 28))
                        bars += width + 4

                    if stamped_ink is not None:
                        ink_image = ink_approved_image if stamped_ink == "APPROVED" else ink_denied_image
                        passport_surface.blit(ink_image, (doc_width - 190, doc_height - 90))

                else:
                    title_text = small_font.render("GALACTIC PASSPORT", True, "black")
                    passport_surface.blit(title_text, (87, 20))
                    passport_surface.blit(mini_photo, (22, 68))
                    passport_surface.blit(field_font.render("CLASS : TRANSIT", True, (30, 34, 42)), (155, 50))
                    passport_surface.blit(field_font.render(f"DOC. ID: #{current_alien.doc_id}", True, (30, 34, 42)), (155, 100))
                    passport_surface.blit(field_font.render("SECTOR: OUTER", True, (30, 34, 42)), (155, 145))

                    passport_surface.blit(field_font.render(f"NAME: {current_alien.passport.name}", True, "black"), (55, 180))
                    passport_surface.blit(field_font.render(f"PLANET: {current_alien.passport.planet}", True, "black"), (55, 230))
                    passport_surface.blit(field_font.render(f"EXPIRES : {current_alien.passport.expiration_date}", True, "black"), (55, 280))
                    passport_surface.blit(field_font.render(f"LIMBS : {current_alien.passport.limbs}", True, "black"), (200, 280))

                    bars = 130
                    for width in [4, 3, 2, 2, 2, 2, 3, 3, 3, 5, 2, 2, 3, 4, 2, 2, 3, 3, 4, 4, 4, 4, 2, 1, 3]:
                        pygame.draw.rect(passport_surface, "black", (bars, 360, width, 36))
                        bars += width + 4

                    if stamped_ink is not None:
                        ink_image = ink_approved_image if stamped_ink == "APPROVED" else ink_denied_image
                        passport_surface.blit(ink_image, (185, 220))

                x_button_close_rect = pygame.Rect(doc_width - 45, 10, 25, 25)
                global_close_button = x_button_close_rect.move(passport_rect.x, passport_rect.y)

                x_button_background = (240, 60, 80) if global_close_button.collidepoint(mouse_pos) else (185, 30, 40)
                pygame.draw.rect(passport_surface, x_button_background, x_button_close_rect, 0, 8)
                pygame.draw.rect(passport_surface, (255, 255, 255), x_button_close_rect, 2, 8)
                x_button_close_text = small_font.render("X", True, "white")
                passport_surface.blit(x_button_close_text, x_button_close_text.get_rect(center=x_button_close_rect.center))

                variable_x = mini_passport_rect.x + (passport_rect.x - mini_passport_rect.x) * passport_scale
                variable_y = mini_passport_rect.y + (passport_rect.y - mini_passport_rect.y) * passport_scale
                scaled_width = max(1, int((doc_width + 12) * passport_scale))
                scaled_height = max(1, int((doc_height + 12) * passport_scale))
                scaled_passport = pygame.transform.scale(passport_surface, (scaled_width, scaled_height))
                screen.blit(scaled_passport, (int(variable_x), int(variable_y)))

            if animation_state == "STAMPING":
                target_spot = passport_rect.center if passport_is_opened else mini_passport_rect.center
                if stamp_timer < 0.22:
                    t = stamp_timer / 0.22
                    eased = t * t
                    sx = 1340 + (target_spot[0] - 1340) * eased
                    sy = target_spot[1] - 45 + 30 * eased
                elif stamp_timer < 0.48:
                    sx, sy = target_spot[0], target_spot[1] - 15
                else:
                    t = (stamp_timer - 0.48) / 0.27
                    sx = target_spot[0] + (1340 - target_spot[0]) * t * t
                    sy = target_spot[1] - 15 - 30 * t

                stamp_rect = stamp_tool_image.get_rect(center=(int(sx), int(sy)))
                screen.blit(stamp_tool_image, stamp_rect)

        elif game_state == "GAME OVER":
            game_over_card = pygame.Rect(310, 130, 660, 460)
            pixel_8_bit_border(screen, game_over_card.move(10, 10), (15, 18, 26), (15, 18, 26), notch=8, border=8)
            pixel_8_bit_border(screen, game_over_card, (34, 40, 54), (220, 45, 65), notch=8, border=8)

            game_over_title = big_font.render("GAME OVER", True, (200, 205, 215))
            screen.blit(game_over_title, game_over_title.get_rect(centerx=640, y=185))

            reason_surface = rule_font.render(game_over_reason, True, (200, 205, 215))
            screen.blit(reason_surface, reason_surface.get_rect(centerx=640, y=265))

            final_score_surface = big_font.render(f"FINAL SCORE: {score}", True, (240, 210, 60))
            screen.blit(final_score_surface, final_score_surface.get_rect(centerx=640, y=335))

            retry_button.draw(screen, mouse_pos, mouse_pressed_true)
            lobby_button.draw(screen, mouse_pos, mouse_pressed_true)

        if shake_timer > 0:
            shake_timer -= dt
            screen.blit(screen.copy(), (random.randint(-6, 6), random.randint(-6, 6)))

        pygame.display.flip()
        await asyncio.sleep(0)
    pygame.quit()
asyncio.run(main())