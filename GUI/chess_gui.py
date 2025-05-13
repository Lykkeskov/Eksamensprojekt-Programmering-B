import pygame
import os
import sys
from points import addPoints


#Initialize Pygame
pygame.init()

#Constants
WIDTH, HEIGHT = 512, 512
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

#Colors
WHITE = (238, 238, 210)
BROWN = (118, 150, 86)
HIGHLIGHT_GREEN = (0, 255, 0, 100)
HIGHLIGHT_RED = (255, 0, 0, 100)
HIGHLIGHT_SELECTED_OUTLINE = (255, 0, 0)

#Load images we have in the assets folder
def load_images():
    pieces = {}
    piece_names = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
    colors = ['w', 'b']
    for color in colors:
        for piece in piece_names:
            path = os.path.join("assets", f"{color}_{piece}.png")
            pieces[f"{color}_{piece}"] = pygame.image.load(path)
    return pieces

#Draw the chessboard
def draw_board(win):
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

#Draw highlight for selected piece with red glow outline
def draw_selected(win, selected):
    if selected:
        row, col = selected
        rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(win, HIGHLIGHT_SELECTED_OUTLINE, rect, 4)  # outline only

#Draw the pieces
def draw_pieces(win, pieces, board, dragging_piece=None, dragging_pos=(0,0), dragging=False, dragging_from=None):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece:
                if dragging and dragging_from == (row, col):
                    continue
                img = pygame.transform.scale(pieces[piece], (SQUARE_SIZE, SQUARE_SIZE))
                win.blit(img, (col * SQUARE_SIZE, row * SQUARE_SIZE))
    if dragging_piece:
        img = pygame.transform.scale(pieces[dragging_piece], (SQUARE_SIZE, SQUARE_SIZE))
        win.blit(img, (dragging_pos[0] - SQUARE_SIZE//2, dragging_pos[1] - SQUARE_SIZE//2))

#Setup the board with so the pieces are at the correct spots
def create_board():
    board = [[None for _ in range(COLS)] for _ in range(ROWS)]
    for i in range(8):
        board[1][i] = 'b_pawn'
        board[6][i] = 'w_pawn'
    pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
    for i in range(8):
        board[0][i] = f'b_{pieces[i]}'
        board[7][i] = f'w_{pieces[i]}'
    return board

#Checkmate screen
#Just a Baic Screen that shows which side won with a return to menu button
def show_checkmate_screen(win, winner):
    font = pygame.font.SysFont("arial", 48)
    text = font.render(f"{winner} Wins by Checkmate!", True, (255, 0, 0))
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    button_font = pygame.font.SysFont("arial", 30)
    btn_text = button_font.render("Return to Menu", True, (255, 255, 255))
    btn_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 50)

    running = True
    while running:
        win.fill((0, 0, 0))
        win.blit(text, rect)
        pygame.draw.rect(win, (100, 100, 100), btn_rect, border_radius=10)
        win.blit(btn_text, btn_text.get_rect(center=btn_rect.center))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn_rect.collidepoint(event.pos):
                    pygame.quit()
                    subprocess.Popen([sys.executable, "main_menu.py"])
                    sys.exit()


#Main function
def main():
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess")
    pieces = load_images()
    board = create_board()
    clock = pygame.time.Clock()
    running = True

    dragging = False
    dragging_piece = None
    dragging_from = None
    dragging_pos = (0, 0)
    selected_square = None

    while running:
        # addPoints() will uncomment when function is done
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col, row = x // SQUARE_SIZE, y // SQUARE_SIZE
                if board[row][col]:
                    dragging = True
                    dragging_piece = board[row][col]
                    dragging_from = (row, col)
                    dragging_pos = event.pos
                    selected_square = (row, col)

            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging:
                    x, y = event.pos
                    new_col, new_row = x // SQUARE_SIZE, y // SQUARE_SIZE
                    old_row, old_col = dragging_from
                    board[old_row][old_col] = None
                    board[new_row][new_col] = dragging_piece
                    dragging = False
                    dragging_piece = None
                    dragging_from = None
                    selected_square = None  # Clear highlight glow after a move has been made

            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    dragging_pos = event.pos

        draw_board(win)
        draw_selected(win, selected_square)
        draw_pieces(win, pieces, board, dragging_piece, dragging_pos, dragging, dragging_from)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
