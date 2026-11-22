import pygame

pygame.init()
LENGTH, HEIGHT = 1280,720
screen = pygame.display.set_mode((LENGTH,HEIGHT))
pygame.display.set_caption("Alien Passport Control")
clock = pygame.time.Clock()
running = True

background = (25,28,38)

while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()