import validMoves


# we distinguish between game outcomes and add points based on it.
def addPoints(points, current_turn, board):
    # used for handling wins/loses/draws
    game_over = False
    winner = None
    loser = None
    points = 0

    status = validMoves.cm_or_sm(board, current_turn)
    if status:
        game_over = True
        if status == "checkmate":
            winner = "w" if current_turn == "b" else "b" # winner id person who delivered the checkmate ofc
            points[winner] += 100
            points[loser] += 25
            print(f"{winner} won by checkmate!")

        else:
            points["w"] += 25
            points["b"] += 25
            print("Stalemate! It's a draw.")
