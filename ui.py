import pygame

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    clock = pygame.time.Clock()

    from alien import Alien
    test_alien = Alien()
    test_rule = "Check the passsport expiration date and species colour"
    #passport
    passport_shadow = pygame.Rect(95,67,390,510)
    passport_rect_border = pygame.Rect(75,50,400,520)
    passport_rect = pygame.Rect(80,55,390,510)
    #approve_button
    approve_button_shadow = pygame.Rect(379,617,270,90)
    approve_button_border = pygame.Rect(360,600,280,100)
    approve_button = pygame.Rect(365,605,270,90)
    #deny_button
    deny_button = pygame.Rect(365,605,570,90)
    deny_button_border = 
    #fonts
    font = pygame.font.Font("assets/fonts/PixelifySans-VariableFont_wght.ttf",28)
    big_font = pygame.font.Font("assets/fonts/PixelifySans-VariableFont_wght.ttf",40)

    alien_img = pygame.image.load("assets/sprites/alien_1.png").convert_alpha()
    alien_img = pygame.transform.scale(alien_img, (192,192))

    running = True
    while running:
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                test_alien = Alien()
            

        pygame.display.set_caption(f"MOUSE: {pygame.mouse.get_pos()}")
        

        screen.fill((173,216,230))
        #PASSPORT
        pygame.draw.rect(screen,(15,17,24),passport_shadow,0,17)
        pygame.draw.rect(screen,"white",passport_rect,0,17)
        pygame.draw.rect(screen,"grey",passport_rect_border,7,17)
        pygame.draw.line(screen,"grey",(120,110),(415,110),3)
        passport_text = font.render("GALACTIC PASSPORT",True, "black")
        screen.blit(passport_text,(passport_rect.x+50,passport_rect.y+20))

        #APPROVE BUTTON
        mouse_pos = pygame.mouse.get_pos()
        hover_colour_approve_button = (50,220,100) if approve_button.collidepoint(mouse_pos) else (30,170,75)

        pygame.draw.rect(screen,(15,17,24),approve_button_shadow,0,17)
        pygame.draw.rect(screen,"green",approve_button,0,20)
        pygame.draw.rect(screen,(0,100,32),approve_button_border,7,20)
        pygame.draw.rect(screen,hover_colour_approve_button, approve_button,0,20)

        approve_button_text = big_font.render("APPROVE", True, "black")
        approve_button_text_center = approve_button_text.get_rect(center = approve_button.center)
        screen.blit(approve_button_text,approve_button_text_center)
        #DENY BUTTON

        #ALIEN IMAGE
        screen.blit(alien_img, (50,75))
        
        
        pygame.display.flip()
    pygame.quit()