import pygame
import os

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 512, 512
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (238, 238, 210)
BROWN = (118, 150, 86)
HIGHLIGHT_GREEN = (0, 255, 0, 100)
HIGHLIGHT_RED = (255, 0, 0, 100)
HIGHLIGHT_SELECTED_OUTLINE = (255, 0, 0)

# Load images
def load_images():
    pieces = {}
    piece_names = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
    colors = ['w', 'b']
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

# Draw highlight for selected piece with red glow outline
def draw_selected(win, selected):
    if selected:
        row, col = selected
        rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(win, HIGHLIGHT_SELECTED_OUTLINE, rect, 4)  # outline only

# Draw the pieces
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

# Setup starting board state
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

# LEGAL move generation (basic)
def get_valid_moves(board, row, col):
    moves = []
    piece = board[row][col]
    if not piece:
        return moves

    color = piece[0]  # 'w' or 'b'
    name = piece[2:]  # e.g., 'pawn'

    def is_enemy(r, c):
        return 0 <= r < ROWS and 0 <= c < COLS and board[r][c] and board[r][c][0] != color

    def is_empty(r, c):
        return 0 <= r < ROWS and 0 <= c < COLS and board[r][c] is None

    directions = {
        'rook':   [(-1,0), (1,0), (0,-1), (0,1)],
        'bishop': [(-1,-1), (-1,1), (1,-1), (1,1)],
        'queen':  [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)],
        'king':   [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]
    }

    if name == 'pawn':
        direction = -1 if color == 'w' else 1
        if is_empty(row + direction, col):
            moves.append((row + direction, col))
            if (color == 'w' and row == 6 or color == 'b' and row == 1) and is_empty(row + 2 * direction, col):
                moves.append((row + 2 * direction, col))
        for dc in [-1, 1]:
            if is_enemy(row + direction, col + dc):
                moves.append((row + direction, col + dc))

    elif name == 'knight':
        knight_moves = [(-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1)]
        for dr, dc in knight_moves:
            r, c = row + dr, col + dc
            if 0 <= r < ROWS and 0 <= c < COLS and (is_empty(r, c) or is_enemy(r, c)):
                moves.append((r, c))

    elif name in ['rook', 'bishop', 'queen']:
        for dr, dc in directions[name]:
            r, c = row + dr, col + dc
            while 0 <= r < ROWS and 0 <= c < COLS:
                if is_empty(r, c):
                    moves.append((r, c))
                elif is_enemy(r, c):
                    moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc

    elif name == 'king':
        for dr, dc in directions['king']:
            r, c = row + dr, col + dc
            if 0 <= r < ROWS and 0 <= c < COLS and (is_empty(r, c) or is_enemy(r, c)):
                moves.append((r, c))

    return moves

# Main function
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
                    selected_square = None  # Clear highlight after move

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
