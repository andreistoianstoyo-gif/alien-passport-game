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
font_button = pygame.font.SysFont("arial", 28, bold = True)
font_title = pygame.font.SysFont("arial", 24, bold = True)

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
background = (25,28,38)

while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if approve_button.collidepoint(event.pos):
                print("Alien APPROVED!")
            elif deny_button.collidepoint(event.pos):
                print("Alien DENIED")
    screen.fill(background)
    pygame.draw.rect(screen, (235,230,215), passport_rect)
    pygame.draw.rect(screen,("green"),approve_button)
    pygame.draw.rect(screen,("red"),deny_button)
    pygame.draw.rect(screen,("blue"),rules_rect)
    text_approve = font_button.render("APPROVED", True, "white")
    screen.blit(text_approve,(approve_button.x + 35, approve_button.y + 15))
    text_deny = font_button.render("DENIED", True, "white")
    screen.blit(text_deny,(deny_button.x + 60, deny_button.y + 15))
    daily_rules = font_button.render("DAILY RULES", True, "yellow")
    screen.blit(daily_rules,(rules_rect.x + 25, rules_rect.y + 10))
    
   
    pygame.display.flip()

    dt = clock.tick(60)/1000

pygame.quit()