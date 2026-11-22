import pygame

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    clock = pygame.time.Clock()

    from alien import Alien
    test_alien = Alien()
    test_rule = "Check the passsport expiration date and species colour"
    passport_rect_border = pygame.Rect(75,50,400,520)
    passport_rect = pygame.Rect(80,55,390,510)
    approve_button_border = pygame.Rect(360,600,300,100)
    approve_button = pygame.Rect(365,605,290,90)
    font = pygame.font.Font


    running = True
    while running:
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                test_alien = Alien()
            

        pygame.display.set_caption(f"MOUSE: {pygame.mouse.get_pos()}")

        screen.fill((25,28,38))
        pygame.draw.rect(screen,"white",passport_rect,0,17)
        pygame.draw.rect(screen,"grey",passport_rect_border,7,17)
        pygame.draw.rect(screen,"green",approve_button,0,20)
        pygame.draw.rect(screen,(0,100,32),approve_button_border,7,20)


        pygame.display.flip()
    pygame.quit()