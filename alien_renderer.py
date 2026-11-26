import os
import pygame
from species_data import PLANETS_SPECIES, CUSTOM_COLOURS
from alien import Alien


PARTS_DIRECTORY = "assets/sprites/parts"
CANVAS_SIZE = (64,64)
PART_CACHE = {}

def load_part(filename):
    if filename in PART_CACHE:
        return PART_CACHE[filename]

    path = os.path.join(PARTS_DIRECTORY,filename)
    if os.path.exists(path):
        image = pygame.image.load(path).convert_alpha()
        if image.get_size() != CANVAS_SIZE:
            image = pygame.transform.scale(image, CANVAS_SIZE)
        PART_CACHE[filename] = image
        return image

    PART_CACHE[filename] = None
    return None

def tint_surface(surface, rgb_colour):
    tinted = surface.copy()
    tint_layer = pygame.Surface(tinted.get_size(), pygame.SRCALPHA)
    tint_layer.fill((*rgb_colour, 255))
    tinted.blit(tint_layer, (0,0), special_flags = pygame.BLEND_RGBA_MULT)
    return tinted

def fallback_support(canvas,category,value,rgb):
    outline = (18,22,30)
    shadow = tuple(max(0, int(c * 0.65))for c in rgb)

    if category == "head":
        pygame.draw.rect(canvas,outline,(18,48,28,16))
        pygame.draw.rect(canvas, shadow, (20,50,24,14))
        pygame.draw.rect(canvas, outline, (14,14,36,36))
        pygame.draw.rect(canvas, rgb, (16,16,32,32))
    elif category == "eyes":
        positons = {
            1: [(32,28)],
            2: [(24,28), (40,28)],
            3: [(32,21), (23,30),(41,30)],
            4: [(23,22), (41,22),(23,31),(41,31)],
            6: [(20, 22), (32, 22), (44, 22), (20, 31), (32, 31), (44, 31)],
            
        }
        for entity_x, entity_y in positons.get(value,positons[2]):
            pygame.draw.rect(canvas, outline, (entity_x -4,entity_y-4, 8,8))
            pygame.draw.rect(canvas,(245,247,255), (entity_x -3, entity_y-3, 6,6))
            pygame.draw.rect(canvas, (15,18,24), (entity_x - 1, entity_y - 1, 3,3))
    elif category == "mouth":
        pygame.draw.rect(canvas,outline,(24,40,16,3))

def render_modular_alien(colour = "green", eyes =2, head = "round", accessory = "antennae", mouth = "smile", target_size = (256,256)):
    canvas = pygame.Surface(CANVAS_SIZE, pygame.SRCALPHA)
    rgb  = CUSTOM_COLOURS.get(colour, (72,205,98))

    accessory_image = load_part(f"accessory_{accessory}.png")
    if accessory_image:
        canvas.blit(accessory_image, (0,0))


    head_image = load_part(f"head_{head}.png")
    if head_image:
        canvas.blit(tint_surface(head_image, rgb), (0,0))
    else:
        fallback_support(canvas, "head", head, rgb)


    eyes_image = load_part(f"eyes_{eyes}.png")
    if eyes_image:
        canvas.blit(eyes_image, (0,0))
    else:
        fallback_support(canvas, "eyes", eyes, rgb)

    mouth_image = load_part(f"mouth_{mouth}.png")
    if mouth_image:
        canvas.blit(mouth_image, (0,0))
    else:
        fallback_support(canvas, "mouth", mouth, rgb)

    return pygame.transform.scale(canvas,target_size)

def render_alien_sprite(alien:Alien, target_size = (256,256)):
    return render_modular_alien(
        colour = alien.colour,
        eyes = alien.eyes,
        head = getattr(alien,"head", "round"),
        accessory = getattr(alien, "accessory", "antennae"),
        mouth = getattr(alien, "mouth", "smile"),
        target_size=target_size,
    )

def render_species_preview(planet_name, target_size = (64,64)):
    traits = PLANETS_SPECIES[planet_name]
    return render_modular_alien(
        colour = traits["colour"],
        eyes = traits["eyes"],
        head = traits.get("head", "round"),
        accessory = traits.get("accessory", "antennae"),
        mouth = "smile",
        target_size=target_size,
    )