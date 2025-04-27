import pygame
import subprocess
import sys


#Setup
pygame.init()
screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption("Chess Online")
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 32)

#Assets
chessboard_img = pygame.image.load("assets/chessboard.png")
chessboard_img = pygame.transform.scale(chessboard_img, (500, 500))

#Colors
BLACK = (30, 30, 30)
WHITE = (255, 255, 255)
GREEN = (170, 225, 70)
DARK_GREY = (60, 60, 60)


#Buttons
def create_button(text, x, y, width, height, color, text_color=WHITE):
    pygame.draw.rect(screen, color, (x, y, width, height), border_radius=10)
    label = font.render(text, True, text_color)
    label_rect = label.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(label, label_rect)
    return pygame.Rect(x, y, width, height)


# Game State
game_state = "main_menu"

# Main Loop
while True:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if game_state == "main_menu":
                if play_online_button.collidepoint(mouse_pos):
                    game_state = "play_options"
                if play_bots_button.collidepoint(mouse_pos):
                    print("Play Bots (not implemented yet)")

            elif game_state == "play_options":
                if join_button.collidepoint(mouse_pos):
                    print("Joining a game...")
                if create_button_rect.collidepoint(mouse_pos):
                    print("Creating a game...")
                if matchmaking_button.collidepoint(mouse_pos):
                    print("Searching for players...")


    if game_state == "main_menu":
        screen.blit(chessboard_img, (50, 50))

        title = font.render("Play Chess Online", True, WHITE)
        title_rect = title.get_rect(center=(850, 100))
        screen.blit(title, title_rect)

        subtitle = small_font.render("on the #1 Site!", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(850, 150))
        screen.blit(subtitle, subtitle_rect)

        play_online_button = create_button("Play Online", 750, 250, 250, 70, GREEN)
        play_bots_button = create_button("Play Bots", 750, 350, 250, 70, DARK_GREY)

    elif game_state == "play_options":
        title = font.render("Choose an Option", True, WHITE)
        title_rect = title.get_rect(center=(600, 100))
        screen.blit(title, title_rect)

        join_button = create_button("Join Game", 475, 200, 250, 70, GREEN)
        create_button_rect = create_button("Create Game", 475, 300, 250, 70, GREEN)
        matchmaking_button = create_button("Matchmaking", 475, 400, 250, 70, GREEN)


    pygame.display.flip()
