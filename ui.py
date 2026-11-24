import pygame
from rules import generate_rules
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
    screen = pygame.display.set_mode((1280,720),pygame.SCALED)
    clock = pygame.time.Clock()

    from alien import Alien
    from rules import generate_rules 
    test_alien = Alien()
    test_rule = "Check the passsport expiration date and species colour"
    #passport
    passport_shadow = pygame.Rect(100,72,390,510)
    passport_rect_border = pygame.Rect(75,50,400,520)
    passport_rect = pygame.Rect(80,55,390,510)
    raw_passport = pygame.image.load("assets/sprites/passport.png").convert_alpha()
    passport_image = pygame.transform.scale_by(raw_passport, 3)
    passport_shadow_image = pygame.mask.from_surface(passport_image).to_surface(
        setcolor=(10,12,18,255),unsetcolor=(0,0,0,0)
    )
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
    small_font = pygame.font.Font("assets/fonts/PixelifySans-VariableFont_wght.ttf",18)
    field_font = pygame.font.Font("assets/fonts/PixelifySans-VariableFont_wght.ttf",16)

    alien_img = pygame.image.load("assets/sprites/alien.png").convert_alpha()
    alien_img = pygame.transform.scale(alien_img, (192,192))
    big_alien_image = pygame.transform.scale(alien_img, (256,256))
    
    
    passport_rect = passport_image.get_rect(topleft=(60,110))  
    mini_passport_rect = pygame.Rect(140,515,110,145)
    passport_is_opened = False

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
    
     #settingssss
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
     
    passport_is_opened = False
    passport_scale = 0
    dragging_passport = False
    drag_offset = (0,0)
        
    running = True
    while running:
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    test_alien = Alien()
                    passport_is_opened = False
                    dragging_passport = False
                if event.key == pygame.K_r:
                    rules_open = not rules_open
                if event.key == pygame.K_ESCAPE:
                    passport_is_opened = False
                    dragging_passport = False
                if event.key == pygame.K_p:
                    passport_is_opened = not passport_is_opened
                    dragging_passport = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if rules_icon_rect.collidepoint(event.pos):
                    rules_open = not rules_open
                if passport_is_opened and passport_scale > 0.9:
                    close_button_rect = pygame.Rect(passport_rect.right -44, passport_rect.y + 10, 34, 34)
                    title_bar_rect = pygame.Rect(passport_rect.x, passport_rect.y, passport_width - 50, 54)
                    if close_button_rect.collidepoint(event.pos):
                        passport_is_opened = False
                        dragging_passport = False
                    elif title_bar_rect.collidepoint(event.pos):
                        dragging_passport = True
                        drag_offset = (passport_rect.x - event.pos[0], passport_rect.y - event.pos[1])
                    elif mini_passport_rect.collidepoint(event.pos):
                        passport_is_opened = False
                elif mini_passport_rect.collidepoint(event.pos):
                    passport_is_opened = True
            if event.type == pygame.MOUSEBUTTONUP and event.button ==1:
                dragging_passport = False
            if event.type == pygame.MOUSEMOTION and dragging_passport:
                passport_rect.x = event.pos[0] + drag_offset[0]
                passport_rect.y = event.pos[1] + drag_offset[1]
                passport_rect.clamp_ip(pygame.Rect(0,0,1280,720))
            if approve_button.clicking(event) or deny_button.clicking(event):
                test_alien = Alien()
                passport_is_opened = False
                dragging_passport = False

        pygame.display.set_caption(f"MOUSE: {pygame.mouse.get_pos()}")
        

        screen.fill((58,68,88))
        mouse_pos = pygame.mouse.get_pos()
        #BACKGROUND
        booth_rect = pygame.Rect(415,35,450,425)
        pixel_8_bit_border(screen,booth_rect,(28,34,46), (35,42,56),notch = 8, border = 8)

        pygame.draw.line(screen, (42,50,66), (450,70),(520,140), 4)
        pygame.draw.line(screen, (42,50,66), (475, 70), (535,130),2)

        alien_booth_rect = big_alien_image.get_rect(center=(640,275))
        screen.blit(big_alien_image,alien_booth_rect)

        pygame.draw.rect(screen, (42,48,62), (0,460,1280,260))
        pygame.draw.rect(screen, (80,90,110), (0,460,1280,16))
        pygame.draw.line(screen, (20,24,32), (0,476), (1280,476), 4)

        for bolts_x in range(40,1280,160):
            pygame.draw.rect(screen, (35,40,45), (bolts_x, 465, 6, 6))
        hovering = 0
        if mini_passport_rect.collidepoint(mouse_pos):
            hovering = -5
        else:
            0

        

        
        #PASSPORT
        

        

    

        #BUTTONS
        
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

        screen.blit(cover_image, (mini_passport_rect.x, mini_passport_rect.y + hovering))
        target_a_scale = 1.0 if passport_is_opened else 0.0
        passport_scale += (target_a_scale - passport_scale) * 20 * dt

        if passport_scale >0.05:
            passport_surface =pygame.Surface((passport_width + 12, passport_height + 12),pygame.SRCALPHA)
            passport_surface.blit(passport_shadow_image, (10,10))
            passport_surface.blit(passport_image,(0,0))

            title_text = font.render("GALACTIC PASSPORT", True, (240,210,60))
            passport_surface.blit(title_text, (95,10))

            mini_photo = pygame.transform.scale(alien_img, (96,96))
            passport_surface.blit(mini_photo, (22,68))

            passport_surface.blit(small_font.render("CLASS:TRANSIT", True, (30,34,42)), (270,66))
            passport_surface.blit(small_font.render("DOCUMENT ID: #13565", True, (30,34,42)), (270, 86))
            passport_surface.blit(small_font.render("SECTOR: OUTER",True, (30,34,42)), (270,106))

            passport_surface.blit(field_font.render(f"NAME: {test_alien.passport.name}", True, "black"),(170,145))
            passport_surface.blit(field_font.render(f"PLANET: {test_alien.passport.planet}", True, "black"),(170,175))
            passport_surface.blit(field_font.render(f"EXPIRES: {test_alien.passport.expiration_date}", True, "black"), (170,205))

            bars_x = 260
            for width in [4,2,2,2,3,2,2,4,5,3,5,2,2,2,3,4,4,4,4,3,2,4,5,3]:
                pygame.draw.rect(passport_surface, "black",(bars_x, 265, width, 36))
                bars_x += width + 4

            x_button_close_rect = pygame.Rect(passport_width - 45, 10, 34,34)
            global_close_button = x_button_close_rect.move(passport_rect.x, passport_rect.y)

            x_button_background = (240,60,80) if global_close_button.collidepoint(mouse_pos) else (185,30,40)
            pygame.draw.rect(passport_surface,x_button_background,x_button_close_rect)
            pygame.draw.rect(passport_surface,(255,255,255),x_button_close_rect,2)
            x_button_close_text = small_font.render("X", True, "white")
            passport_surface.blit(x_button_close_text,x_button_close_text.get_rect(center = x_button_close_rect.center))

            variable_x = mini_passport_rect.x + (passport_rect.x - mini_passport_rect.x) * passport_scale
            variable_y = mini_passport_rect.y + (passport_rect.y - mini_passport_rect.y) * passport_scale
            scaled_width = max(1, int((passport_width + 12)*passport_scale))
            scaled_height = max(1, int((passport_height + 12)*passport_scale))
            scaled_passport = pygame.transform.scale(passport_surface, (scaled_width,scaled_height))
            screen.blit(scaled_passport,(int(variable_x),int(variable_y)))

        pygame.display.flip()
    pygame.quit()