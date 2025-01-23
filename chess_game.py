import chess
import datetime
import os

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 30)
    print(" " * 10 + "Namaste!!!" + " " * 10)
    print("=" * 30)
    print("\nH - Help (Use H for help)\n")
    input("Press Enter to start the game...\n")

    white_player = input("Enter White's name: ").strip()
    black_player = input("Enter Black's name: ").strip()
    display_instructions()

    board = chess.Board()
    while not board.is_game_over():
        display_board(board)
        print(f"\nCurrent turn: {'White' if board.turn else 'Black'}")
        move = get_move(board)
        if move:
            board.push(move)
            handle_promotion(board)

    display_board(board)
    result = "1-0" if not board.turn else "0-1" if board.is_checkmate() else "1/2-1/2"

    if board.is_checkmate():
        print(f"\nCheckmate! {'White' if result == '1-0' else 'Black'} wins!\n")
    elif board.is_stalemate():
        print("\nStalemate! It's a draw.\n")
    elif board.is_insufficient_material():
        print("\nDraw due to insufficient material.\n")
    else:
        print("\nGame over (unknown reason).\n")

    pgn = generate_pgn(board, white_player, black_player, result)
    print("\nPGN for the game:\n")
    print(pgn)

    save = input("\nWould you like to save this game? (y/n): ").lower()
    if save == "y":
        folder_name = "Chess_PGN"
        os.makedirs(folder_name, exist_ok=True)
        file_name = f"{folder_name}/chess_game_{datetime.datetime.now().strftime('%d%m%Y_%H%M%S')}.txt"
        with open(file_name, "w") as f:
            f.write(pgn)
        print(f"\nGame saved to '{file_name}'.\n")
    print("\nGame Over. Thanks for playing!\n")

def display_instructions():
    """Displays instructions on how to play the chess game in algebraic notation."""
    print("\n\n=== Instructions ===\n")
    print("This chess game uses Algebraic Notation. Here's a quick guide:")
    print("1. **Piece Symbols**: K: King, Q: Queen, R: Rook, B: Bishop, N: Knight.")
    print("   Pawns are not labeled (e.g., 'e4' means a pawn moves to 'e4').")
    print("2. **Captures**: Include `x` before the destination square (e.g., Nxf6).")
    print("3. **Special Moves**: O-O for kingside castling, O-O-O for queenside.")
    print("4. **Promotion**: Add '=' and promoted piece (e.g., e8=Q).")
    print("5. **Checks and Checkmate**: + for check (e.g., Qh5+), # for checkmate.")
    print("6. **Undo Move**: Type 'undo' to undo the last move.")
    print("7. **Exit Game**: Type 'exit' or 'q' to quit the game gracefully.")
    print("\nUse correct notation and have fun playing!\n")

def display_help_menu():
    """Displays a help menu with available commands during the game."""
    print("\n\n=== Help Menu ===\n")
    print("1. I, Ins or Instructions - Type 'I' to display Chess Notation Instructions.")
    print("2. Undo or U - To undo the last move.")
    print("3. Exit, E or Q - To exit the game gracefully.")
    print("\nUse these commands anytime during your turn.\nNote: These commands are not case-sensitive.\n")

def display_board(board):
    """Displays the current state of the chess board."""
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal screen for better readability
    print("\n   a b c d e f g h")  # X-axis labels (columns)
    print("  +-----------------+")
    board_rows = str(board).split("\n")
    for i, row in enumerate(board_rows):
        print(f"{8-i} | {row} | {8-i}")  # Y-axis labels (rows)
    print("  +-----------------+")
    print("   a b c d e f g h")  # X-axis labels (columns)
    print("\n")

def get_move(board):
    """Prompts the player to input a valid move and validates it."""
    while True:
        move_input = input("\nEnter your move: ").strip()
        if move_input.lower() in {"h", "help"}:
            display_help_menu()
            continue
        if move_input.upper() in {"I", "ins", "instructions"}:
            display_instructions()
            continue
        if move_input.lower() in {"undo", "u"}:
            if len(board.move_stack) > 0:
                board.pop()
                print("\nLast move undone!\n")
                return None
            else:
                print("\nNo moves to undo!\n")
                continue
        if move_input.lower() in {"exit", "q", "e"}:
            print("\nGame exited. Thanks for playing!\n")
            exit(0)  # Exit gracefully

        try:
            move = board.parse_san(move_input)
            if move in board.legal_moves:
                return move
            else:
                print("\nIllegal move! Try again.\n")
        except ValueError:
            print("\nInvalid move! Use correct algebraic notation (e.g., e4, Nf3, O-O).\n")

def handle_promotion(board):
    """Handles the promotion of pawns when they reach the opposite end of the board."""
    if board.is_game_over():
        return
    last_move = board.peek()
    promotion_square = last_move.to_square
    if chess.square_rank(promotion_square) in {0, 7} and board.piece_type_at(promotion_square) == chess.PAWN:
        while True:
            choice = input("\nPawn promotion! Choose (Q, R, B, N): ").upper()
            if choice in {"Q", "R", "B", "N"}:
                promotion_piece = {
                    "Q": chess.QUEEN,
                    "R": chess.ROOK,
                    "B": chess.BISHOP,
                    "N": chess.KNIGHT
                }[choice]
                board.remove_piece_at(promotion_square)
                board.set_piece_at(promotion_square, chess.Piece(promotion_piece, board.turn))
                print(f"\nPawn promoted to {choice}!\n")
                break
            else:
                print("\nInvalid choice! Please select Q, R, B, or N.\n")

def generate_pgn(board, white_player, black_player, result):
    """Generates a PGN (Portable Game Notation) formatted string representing the game."""
    event = "Battle of Minds | Chess"
    date = datetime.datetime.now().strftime("%d.%m.%Y")
    termination = ""

    if board.is_checkmate():
        termination = f"{'Black' if board.turn else 'White'} wins by checkmate"
    elif board.is_stalemate():
        termination = "Draw by stalemate"
        result = "1/2-1/2"
    elif board.is_insufficient_material():
        termination = "Draw due to insufficient material"
        result = "1/2-1/2"
    else:
        termination = "Game over (unknown reason)"

    pgn = f'[Event "{event}"]\n[Date "{date}"]\n[White "{white_player}"]\n'
    pgn += f'[Black "{black_player}"]\n[Result "{result}"]\n[Termination "{termination}"]\n\n'

    moves = list(board.move_stack)
    san_moves = []
    temp_board = chess.Board()
    for move in moves:
        san_moves.append(temp_board.san(move))
        temp_board.push(move)

    for i in range(0, len(san_moves), 2):
        pgn += f"{(i // 2) + 1}. {san_moves[i]}"
        if i + 1 < len(san_moves):
            pgn += f" {san_moves[i + 1]}"
        pgn += " "
    return pgn.strip()

if __name__ == "__main__":
    main()
