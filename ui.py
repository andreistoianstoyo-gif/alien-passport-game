import pygame
class PixelButton:
    def __init__(s,x,y,width,height,text,font,base_colour,hover_colour,border_colour):
        s.rect = pygame.Rect(x,y,width,height)
        s.text = text
        s.font = font
        s.base_colour = base_colour
        s.hover_colour = hover_colour
        s.border_colour = border_colour
        s.offset = 0




    def draw(s, screen, mouse_pos, pressed_true):
        hovered_true = s.rect.collidepoint(mouse_pos)
        clicked_true = hovered_true and pressed_true[0]
        #click animation
        if clicked_true:
            offset_value = 6
        elif hovered_true:
            offset_value = 2
        else:
            offset_value = 0
        s.offset += (offset_value - s.offset) * 0.2

        #fixed shadow(8-bit style x)
        shadow_rect = pygame.Rect(s.rect.x + 10,s.rect.y + 10,s.rect.width,s.rect.height)
        pygame.draw.rect(screen, (10,12,18), shadow_rect)

        #the button duh
        button_surface = pygame.Surface((s.rect.width,s.rect.height))
        if hovered_true:
            direct_colour = s.hover_colour
        else:
            direct_colour = s.base_colour
        button_surface.fill(direct_colour)

        #border colour
        pygame.draw.rect(button_surface, s.border_colour, (0,0,s.rect.width,s.rect.height),7)
        pygame.draw.line(button_surface,(240,240,240), (7,7), (s.rect.width-8,7),3)
        pygame.draw.line(button_surface,(240,240,240),(7,7),(7,s.rect.height-8),3)

        #centered textt
        text = s.font.render(s.text, True, "black")
        text_rect = text.get_rect(center=(s.rect.width//2,s.rect.height//2))
        button_surface.blit(text, text_rect)

        #drawing
        offset = int(s.offset)
        screen.blit(button_surface, (s.rect.x + offset, s.rect.y + offset))

    def clicking(s,event):
        return(
            event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and s.rect.collidepoint(event.pos)
            )

def pixel_8_bit_border(surface, rect, inside_colour, border_colour, notch = 6, border = 6):
        pygame.draw.rect(surface, border_colour, (rect.x,rect.y + notch, rect.width, rect.height - notch *2 ))
        pygame.draw.rect(surface,border_colour,(rect.x+notch,rect.y, rect.width - notch*2, rect.height))

        inside_x, inside_y = rect.x + border, rect.y + border
        inside_width, inside_height = rect.width - border*2, rect.height - border*2
        inside_notch = max(2, notch-2)

        pygame.draw.rect(surface,inside_colour,(inside_x,inside_y + inside_notch, inside_width, inside_height - inside_notch*2))
        pygame.draw.rect(surface,inside_colour,(inside_x + inside_notch, inside_y, inside_width - inside_notch *2,inside_height))    

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    clock = pygame.time.Clock()

    from alien import Alien
    from rules import generate_rules 
    test_alien = Alien()
    test_rule = "Check the passsport expiration date and species colour"
    #passport
    passport_shadow = pygame.Rect(100,72,390,510)
    passport_rect_border = pygame.Rect(75,50,400,520)
    passport_rect = pygame.Rect(80,55,390,510)
    #approve_button
    approve_button_shadow = pygame.Rect(294,627,270,90)
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
    rule_font = pygame.font.Font("assets/fonts/PixelifySans-VariableFont_wght.ttf",24)

    alien_img = pygame.image.load("assets/sprites/alien_1.png").convert_alpha()
    alien_img = pygame.transform.scale(alien_img, (192,192))

    rules_icon = pygame.image.load("assets/sprites/rules.png").convert_alpha()
    rules_icon = pygame.transform.scale(rules_icon,(192,192))
    rules_icon_rect = rules_icon.get_rect(topright=(1305,0))
    rules_open = True
    rules_scale = 1.0
    screen.blit(rules_icon, rules_icon_rect)

    def not_unbound_text(surface, text, font,colour,rect,start_y):
        words = text.split(" ")
        line = ""
        y = start_y
        max_width = rect.width - 40

        for word in words:
            test_line = line + word + " "
            if font.size(test_line)[0] <= max_width:
                line = test_line
            else:
                rendered = font.render(line,True,colour)
                surface.blit(rendered, (rect.x + 20, y))
                line = word + " "
                y += font.get_linesize() + 4
        if line:
            rendered = font.render(line, True, colour)
            surface.blit(rendered,(rect.x + 20, y))
    current_rule = generate_rules()["RULE"]
    
    approve_button = PixelButton(300,605,270,90,"APPROVE", big_font, (0,200,0),(50,240,100), (0,100,32))
    deny_button = PixelButton(700,605,280,90, "DENY", big_font, (200,0,0), (240,50,100), (100,0,32))


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
            
            if approve_button.clicking(event) or deny_button.clicking(event):
                test_alien = Alien()
        pygame.display.set_caption(f"MOUSE: {pygame.mouse.get_pos()}")
        

        screen.fill((58,68,88))
        #PASSPORT
        passport_text = font.render("GALACTIC PASSPORT",True, "black")
        pixel_8_bit_border(screen,passport_shadow,"black","black", notch = 8, border = 6)
        pixel_8_bit_border(screen,passport_rect,"white","grey",notch = 6,border = 6)

        passport_text - font.render("GALACTIC PASSPORT", True, "black")
        screen.blit(passport_text, (passport_rect.x + 48, passport_rect.y + 18))
        pygame.draw.line(screen,"grey",(passport_rect.x + 25,passport_rect.y + 56),(passport_rect.right - 25, passport_rect.y + 56), 3)

        photo_rect = pygame.Rect(passport_rect.x + 25, passport_rect.y + 70, 120,125)
        pygame.draw.rect(screen,(220,225,230),photo_rect)
        pygame.draw.rect(screen. "grey", photo_rect,4)
        mini_photo = pygame.transform.scale(alien_img,(100,100))
        screen.blit(mini_photo, (photo_rect.x + 0, photo_rect.y + 12))

        screen.blit(rule_font.render("CLASS: TRANSIT", True, (90,95,105)),(passport_rect.x + 160, passport_rect.y + 75))
        screen.blit(rule_font.render("DOCUMENT ID: #42351", True, (90,95,105)),(passport_rect.x + 160, passport_rect.y +100))
        screen.blit(rule_font.render("SECTOR: OUTER GALAXY", True, (90,95,105)),(passport_rect.x+160, passport_rect.y+150))

        fields = [
            ("FULL NAME", test_alien.passport.name, passport_rect.y + 200),
            ("ORIGIN PLANET", test_alien.passport.planet, passport_rect.y + 270)
            ("EXPIRATION YEAR", str(test_alien.passport.expiration_date), passport_rect.y + 340)
        ]

        

        #BUTTONS
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed_true = pygame.mouse.get_pressed()
        approve_button.draw(screen,mouse_pos, mouse_pressed_true)
        deny_button.draw(screen, mouse_pos, mouse_pressed_true)
        
        
        
        

        #DAILY RULES
        
        if rules_icon_rect.collidepoint(mouse_pos):
            screen.blit(rules_icon, (rules_icon_rect.x,rules_icon_rect.y-3))
        else:
            screen.blit(rules_icon, rules_icon_rect)

        target_scale = 1.0 if rules_open else 0.0
        rules_scale += (target_scale - rules_scale) * 20 * dt



        if rules_scale > 0.05:
            WIDTH, HEIGHT = 290 , 480
            TRANSPARENT_BORDER = 14
            rules_surface = pygame.Surface((WIDTH + 15,HEIGHT + 15 + TRANSPARENT_BORDER),pygame.SRCALPHA)

            pygame.draw.rect(rules_surface, (15,17,24),(15,15+TRANSPARENT_BORDER,WIDTH,HEIGHT),0,17)
            pygame.draw.rect(rules_surface, (0,190,230),(0,TRANSPARENT_BORDER,WIDTH,HEIGHT),0,17)
            pygame.draw.rect(rules_surface, (10,75,220),(0,TRANSPARENT_BORDER,WIDTH+3,HEIGHT+3),7,20)
            

            rules_title = font.render("DAILY RULES", True, "black")
            rules_title_rect = rules_title.get_rect(centerx = WIDTH//2, y = 20+TRANSPARENT_BORDER)
            rules_surface.blit(rules_title, rules_title_rect)
            pygame.draw.line(rules_surface, (12,17,24), (25,55+TRANSPARENT_BORDER),(WIDTH - 25, 55 + TRANSPARENT_BORDER),3)
            pygame.draw.line(rules_surface, (200,200,0),(100,3+TRANSPARENT_BORDER),(WIDTH - 100,3+TRANSPARENT_BORDER),7)
            pygame.draw.line(rules_surface, (220,220,0),(100,TRANSPARENT_BORDER),(WIDTH-100,TRANSPARENT_BORDER),12)
            pygame.draw.line(rules_surface, (220,220,0),(100,TRANSPARENT_BORDER),(WIDTH-100,TRANSPARENT_BORDER),12)
            
            not_unbound_text(
                rules_surface,
                f"RULE 1: {current_rule}",
                rule_font,
                "black",
                pygame.Rect(0,0,WIDTH,HEIGHT),
                75,
            )
            
            NEW_WIDTH = max(1,int(WIDTH * rules_scale))
            NEW_HEIGHT = max(1,int(HEIGHT * rules_scale))
            scaled_panel = pygame.transform.scale(rules_surface, (NEW_WIDTH,NEW_HEIGHT))

            scaled_rect = scaled_panel.get_rect(topright=(1250,30))
            screen.blit(scaled_panel, scaled_rect)

        
        
        pygame.display.flip()
    pygame.quit()