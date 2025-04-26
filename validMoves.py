import copy

# short for "valid moves without check"
# is like valid_moves(), but does not call is_in_check() recursively
# recursive is when "a function calls itself to solve a problem, breaking it down into smaller, manageable subproblems"
# wow such fancy wording
def vmwc(piece, col, row, board):
    moves = [] # list for storing legal moves
    color, kind = piece.split('_') # splits the name of the piece into color and kind

    # squares/slots in the grid
    def square_in_grid(x, y):
        return 0 <= x < 8 and 0 <= y < 8

    # pawn valid moves
    if kind == "pawn":
        direction = -1 if color == "w" else 1 # controls if it should move up or down, depending on the color
        start_row = 6 if color == "w" else 1 # used to allow it to move 2 slots on first move

        # Movement (1 slot forward if its empty). checks if square_in_grid to avoid indexing errors
        if square_in_grid(col, row + direction) and board[row + direction][col] is None:
            moves.append((col, row + direction))
            # Ability to move 2 slots first time (checks if start_row and if next anf second next slots are empty)
            if row == start_row and board[row + 2 * direction][col] is None:
                    moves.append((col, row + 2 * direction))

        # kill/capture rules (diagonal, one slot)
        for dx in [-1, 1]:
            new_col = col + dx
            new_row = row + direction
            if square_in_grid(new_col, new_row): # must not be out of bounds, so on the grid
                target = board[new_row][new_col]
                if target and target[0] != color: # check if same color or not, so we cant capture own pieces
                    moves.append((new_col, new_row))


    # knight valid moves
    elif kind == "knight":
        possible_moves = [
            (1, 2), (2, 1), (2, -1), (1, -2),
            (-1, -2), (-2, -1), (-2, 1), (-1, 2)
        ] # row and column offset from current pos (the deltas are L shaped here)
        for dx, dy in possible_moves:
            new_col, new_row = col + dx, row + dy
            # Check if new pos is a valid slot, if so then set target
            if square_in_grid(new_row, new_col):
                target = board[new_col][new_row]
                if target is None or target[0] != color:
                    moves.append((new_col, new_row))

    # king valid moves
    elif kind == "king":
        possible_moves = [
            (-1, -1), (-1, 0), (-1, 1), (0, -1),
            (0, 1), (1, -1), (1, 0), (1, 1)
        ] # possible deltas are 1 in every direction
        for dx, dy in possible_moves:
            new_col = col + dx
            new_row = row + dy
            if square_in_grid(new_col, new_row):
                target = board[new_row][new_col]
                if target is None or target[0] != color:
                    moves.append((new_col, new_row))


    # rook, bishop and queen valid moves
    # valid moves for queen is just valid moves for rook + bishop
    # condensed to save lines of code
    elif kind in ['rook', 'bishop', 'queen']:
        directions = []
        if kind in ['rook', 'queen']:
            directions += [(1, 0), (-1, 0), (0, 1), (0, -1)]
        if kind in ['bishop', 'queen']:
            directions += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in directions:
            # directions are handled in a for loop
            for i in range(1, 8):
                new_col, new_row = col + dx * i, row + dy * i
                if not square_in_grid(new_col, new_row):
                    break
                target = board[new_row][new_col]
                if target is None:
                    moves.append((new_col, new_row))
                elif target[0] != color:
                    moves.append((new_col, new_row))
                    break
                else:
                    break

    return moves


# here we use the copy library that we imported at the start
def would_cause_check(piece, col, row, move, board):
    simulated_board = copy.deepcopy(board)

    new_col, new_row = move
    simulated_board[row][col] = None
    simulated_board[new_col][new_row] = piece
    color, _ = piece.split('_')

    # find the kings position
    king_pos = None # set it to none by default
    for r in range(8):
        for c in range(8):
            current_piece = simulated_board[r][c]
            if simulated_board[r][c] == f"{color}_king": # if the dude is on the board
                king_pos = (r, c) # we get his location (fbi type beat)
                break
        if king_pos:
            break
    if not king_pos:
        return True # oh no, king is missing

    king_col, king_row = king_pos

    for r in range(8):
        for c in range(8):
            enemy_piece = simulated_board[r][c]
            if enemy_piece and enemy_piece[0] != color:
                enemy_moves = vmwc(enemy_piece, col, row, simulated_board)
                if (king_col, king_row) in enemy_moves: #checks in enemy_moves attach the king
                    return True
    return False


def valid_moves(piece, col, row, board):
    moves = vmwc(piece, col, row, board)
    legal_moves = []
    for move in moves:
        if not would_cause_check(piece, col, row, move, board):
            legal_moves.append(move)
    return legal_moves



def in_check(board, color):
    # first find the king
    king_pos = None # set it to none by default
    for r in range(8):
        for c in range(8):
            if board[r][c] == f"{color}_king": # if the dude is on the board
                king_pos = (r, c) # we get his location (fbi type beat)
                break
        if king_pos:
            break
    if not king_pos:
        return True

    enemy_color = 'b' if color == 'w' else 'w' # set the color of enemy to opposite of one self

    # check all enemy pieces
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece and piece[0] == enemy_color:
                moves = vmwc(piece, c, r, board)
                if king_pos in moves:
                    return True
    return False


# short for checkmate or stalemate
def cm_or_sm(board, color):
    # if there's no legal moves for any piece
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece and piece[0] == color:
                if valid_moves(piece, col, row, board):
                    return None # still aint no legal moved

    if in_check(color, board):
        return "checkmate"
    else:
        return "stalemate"
