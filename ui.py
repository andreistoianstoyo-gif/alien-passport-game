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
