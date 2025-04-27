import pygame
import sys

pygame.init()

# Window setup
WIDTH, HEIGHT = 1200, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Online")

# Colors
BG_COLOR = (30, 30, 30)
GREEN = (139, 195, 74)
DARK_GREEN = (120, 170, 60)
GRAY = (60, 60, 60)
DARK_GRAY = (45, 45, 45)
WHITE = (255, 255, 255)

# Fonts
title_font = pygame.font.SysFont("Arial", 64, bold=True)
subtext_font = pygame.font.SysFont("Arial", 24)
button_font = pygame.font.SysFont("Arial", 32, bold=True)

# Load chessboard image
chessboard_img = pygame.image.load("assets/chessboard.png")  # << your image name here
chessboard_img = pygame.transform.scale(chessboard_img, (500, 500))  # scale to fit nicely

# Button class
class Button:
    def __init__(self, x, y, width, height, color, hover_color, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text

    def draw(self, win):
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(mouse_pos)
        pygame.draw.rect(win, self.hover_color if is_hover else self.color, self.rect, border_radius=10)

        text_surf = button_font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        win.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

# Create buttons
play_online_button = Button(800, 300, 300, 70, GREEN, DARK_GREEN, "Play Online")
play_bots_button = Button(800, 400, 300, 70, GRAY, DARK_GRAY, "Play Bots")

# Main loop
running = True
while running:
    win.fill(BG_COLOR)

    # Draw chessboard
    win.blit(chessboard_img, (50, 50))

    # Title
    title_text = title_font.render("Play Chess Online", True, WHITE)
    title_rect = title_text.get_rect(center=(950, 100))
    win.blit(title_text, title_rect)

    subtext = subtext_font.render("on the #1 Site!", True, WHITE)
    subtext_rect = subtext.get_rect(center=(950, 160))
    win.blit(subtext, subtext_rect)

    # Buttons
    play_online_button.draw(win)
    play_bots_button.draw(win)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if play_online_button.is_clicked(event):
            print("Play Online clicked!")
        if play_bots_button.is_clicked(event):
            print("Play Bots clicked!")

    pygame.display.update()

pygame.quit()
sys.exit()
