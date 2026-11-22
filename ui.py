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
    approve_button_shadow = pygame.Rect(284,617,270,90)
    approve_button_border = pygame.Rect(265,600,280,100)
    approve_button = pygame.Rect(270,605,270,90)
    #deny_button
    deny_button_shadow = pygame.Rect(754,617,270,90)
    deny_button_border = pygame.Rect(735,600,280,100)
    deny_button = pygame.Rect(740,605,270,90)
    #daily rules
    rules_shadow = pygame.Rect(964,62,300,500)
    rules_border = pygame.Rect(945,45,310,510)
    rules = pygame.Rect(950,50,300,500)
    #fonts
    font = pygame.font.Font("assets/fonts/PixelifySans-VariableFont_wght.ttf",28)
    big_font = pygame.font.Font("assets/fonts/PixelifySans-VariableFont_wght.ttf",40)

    alien_img = pygame.image.load("assets/sprites/alien_1.png").convert_alpha()
    alien_img = pygame.transform.scale(alien_img, (192,192))

    rules_icon = pygame.image.load("assets/sprites/rules.png").convert_alpha()
    rules_icon = pygame.transform.scale(rules_icon,(64,64))
    rules_icon_rect = rules_icon.get_rect(topright=(1230,30))
    rules_open = True
    rules_scale = 1.0
    screen.blit(rules_icon, rules_icon_rect)

    running = True
    while running:
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                test_alien = Alien()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if rules_icon_rect.collidepoint(event.pos):
                    rules_open = not rules_open
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                rules_open = not rules_open
            
        target_scale = 1.0 if rules_open else 0.2
        rules_scale += (target_scale - rules_scale) * 12 * dt

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
        mouse_pos_approve_button = pygame.mouse.get_pos()
        hover_colour_approve_button = (50,240,100) if approve_button.collidepoint(mouse_pos_approve_button) else (0,200,0)

        pygame.draw.rect(screen,(15,17,24),approve_button_shadow,0,17)
        pygame.draw.rect(screen,(0,128,0),approve_button,0,20)
        pygame.draw.rect(screen,(0,100,32),approve_button_border,7,20)
        pygame.draw.rect(screen,hover_colour_approve_button, approve_button,0,20)

        approve_button_text = big_font.render("APPROVE", True, "black")
        approve_button_text_center = approve_button_text.get_rect(center = approve_button.center)
        screen.blit(approve_button_text,approve_button_text_center)
        
        #DENY BUTTON
        mouse_pos_deny_button = pygame.mouse.get_pos()
        hover_colour_deny_button = (240,50,100) if deny_button.collidepoint(mouse_pos_deny_button) else (200,0,0)

        pygame.draw.rect(screen,(15,17,24),deny_button_shadow,0,17)
        pygame.draw.rect(screen,(240,50,100),deny_button,0,20)
        pygame.draw.rect(screen,(100,0,32),deny_button_border,7,20)
        pygame.draw.rect(screen,hover_colour_deny_button,deny_button,0,20)

        deny_button_text = big_font.render("DENY",True,"black")
        deny_button_text_center = deny_button_text.get_rect(center= deny_button.center)
        screen.blit(deny_button_text,deny_button_text_center)

        #DAILY RULES
        pygame.draw.rect(screen,(15,17,24),rules_shadow,0,17)
        pygame.draw.rect(screen,(246,236,215),rules,0,17)
        pygame.draw.rect(screen,(125,87,46),rules_border,7,20)

        rules_text = font.render("DAILY RULES", True, "black")
        screen.blit(rules_text,(rules.x + 67,rules.y + 30))


        

        
        

        if rules_scale > 0.05:
            WIDTH, HEIGHT = 300,480
            rules_surface = pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)

            pygame.draw.rect(rules_surface,(20,20,20,20), (0,0,WIDTH,HEIGHT),0,17)
            pygame.draw.rect(rules_surface,(0,200,200), (0,0,WIDTH,HEIGHT),0,17)

            title = font.render("DAILY RULES", True, (0,200,220))
            rules_surface.blit(title,(45,45))

            NEW_WIDTH = max(1,int(WIDTH * rules_scale))
            NEW_HEIGHT = max(1,int(HEIGHT * rules_scale))
            scaled_panel = pygame.transform.scale(rules_surface, (NEW_WIDTH,NEW_HEIGHT))

            scaled_rect = scaled_panel.get_rect(topright=(rules_icon_rect.right, rules_icon_rect.bottom + 30))
            screen.blit(scaled_panel, scaled_rect)

        #ALIEN IMAGE
        screen.blit(alien_img, (50,75))
        
        
        pygame.display.flip()
    pygame.quit()