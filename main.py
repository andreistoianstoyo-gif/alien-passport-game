import pygame

pygame.init()
LENGTH, HEIGHT = 1280,720
screen = pygame.display.set_mode((LENGTH,HEIGHT))
pygame.display.set_caption("Alien Passport Control")
clock = pygame.time.Clock()
running = True
dt = 0
passport_rect = pygame.Rect(100,30,420,480)
approve_button = pygame.Rect(350,625,225,60)
deny_button = pygame.Rect(700,625,225,60)
rules_rect = pygame.Rect(1000,50,225,550)


player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
background = (25,28,38)

while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background)
    pygame.draw.rect(screen, (235,230,215), passport_rect)
    pygame.draw.rect(screen,("green"),approve_button)
    pygame.draw.rect(screen,("red"),deny_button)
    pygame.draw.rect(screen,("blue"),rules_rect)
   
    pygame.display.flip()

    dt = clock.tick(60)/1000

pygame.quit()