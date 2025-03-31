import pygame
import os

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 512, 512  # 64x64 squares
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (238, 238, 210)
BROWN = (118, 150, 86)


# Load images
def load_images():
    pieces = {}
    piece_names = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
    colors = ['w', 'b']  # White and Black
    for color in colors:
        for piece in piece_names:
            path = os.path.join("assets", f"{color}_{piece}.png")
            pieces[f"{color}_{piece}"] = pygame.image.load(path)
    return pieces


# Draw the chessboard
def draw_board(win):
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


# Draw the pieces
def draw_pieces(win, pieces):
    piece_positions = {
        "w_pawn": [(i, 6) for i in range(8)],
        "b_pawn": [(i, 1) for i in range(8)],
        "w_rook": [(0, 7), (7, 7)], "b_rook": [(0, 0), (7, 0)],
        "w_knight": [(1, 7), (6, 7)], "b_knight": [(1, 0), (6, 0)],
        "w_bishop": [(2, 7), (5, 7)], "b_bishop": [(2, 0), (5, 0)],
        "w_queen": [(3, 7)], "b_queen": [(3, 0)],
        "w_king": [(4, 7)], "b_king": [(4, 0)],
    }
    for piece, positions in piece_positions.items():
        for col, row in positions:
            img = pygame.transform.scale(pieces[piece], (SQUARE_SIZE, SQUARE_SIZE))
            win.blit(img, (col * SQUARE_SIZE, row * SQUARE_SIZE))


# Main function
def main():
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess")
    pieces = load_images()
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_board(win)
        draw_pieces(win, pieces)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
