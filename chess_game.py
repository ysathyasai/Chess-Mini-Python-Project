import chess
import datetime
import os

def main():
    # Clear the terminal screen at the start of the program for better readability
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Print a welcome message with a decorative border
    print("=" * 30)
    print(" " * 10 + "Namaste!!!" + " " * 10)
    print("=" * 30)
    
    # Prompt the user to press Enter to start the game
    print("\nH - Help (Use H for help)\n")
    input("Press Enter to start the game...\n")

    # Get the names of the players
    white_player = input("Enter White's name: ").strip()
    black_player = input("Enter Black's name: ").strip()
    
    # Display the instructions for the game
    display_instructions()

    # Initialize a new chess board
    board = chess.Board()
    
    # Main game loop, continues until the game is over
    while not board.is_game_over():
        # Display the current state of the board
        display_board(board)
        
        # Indicate whose turn it is (White or Black)
        print(f"\nCurrent turn: {'White' if board.turn else 'Black'}")
        
        # Get a move from the player and validate it
        move = get_move(board)
        
        # If a valid move is provided, push it to the board
        if move:
            board.push(move)
            # Handle pawn promotion if applicable
            handle_promotion(board)

    # Display the final state of the board
    display_board(board)
    
    # Determine the result of the game
    result = "1-0" if not board.turn else "0-1" if board.is_checkmate() else "1/2-1/2"

    # Print the result based on the game outcome
    if board.is_checkmate():
        print(f"\nCheckmate! {'White' if result == '1-0' else 'Black'} wins!\n")
    elif board.is_stalemate():
        print("\nStalemate! It's a draw.\n")
    elif board.is_insufficient_material():
        print("\nDraw due to insufficient material.\n")
    else:
        print("\nGame over (unknown reason).\n")

    # Generate the PGN (Portable Game Notation) for the game
    pgn = generate_pgn(board, white_player, black_player, result)
    
    # Print the PGN of the game
    print("\nPGN for the game:\n")
    print(pgn)

    # Ask the user if they want to save the game
    save = input("\nWould you like to save this game? (y/n): ").lower()
    
    if save == "y":
        # Create a folder to save the PGN files if it doesn't exist
        folder_name = "Chess_PGN"
        os.makedirs(folder_name, exist_ok=True)
        
        # Generate a unique filename based on the current date and time
        file_name = f"{folder_name}/chess_game_{datetime.datetime.now().strftime('%d%m%Y_%H%M%S')}.txt"
        
        # Save the PGN to the file
        with open(file_name, "w") as f:
            f.write(pgn)
        
        # Inform the user that the game has been saved
        print(f"\nGame saved to '{file_name}'.\n")
    
    # Thank the user for playing and end the game
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
    print("8. **Clear Board**: Type 'c' or 'clear' to clear and print the current board state.")
    print("\nUse correct notation and have fun playing!\n")

def display_help_menu():
    """Displays a help menu with available commands during the game."""
    print("\n\n=== Help Menu ===\n")
    print("1. I, Ins or Instructions - Type 'I' to display Chess Notation Instructions.")
    print("2. Undo or U - To undo the last move.")
    print("3. Exit, E or Q - To exit the game gracefully.")
    print("4. Clear or C - To clear and print the current board state.")
    print("\nUse these commands anytime during your turn.\nNote: These commands are not case-sensitive.\n")

def display_board(board):
    """Displays the current state of the chess board."""
    # Clear the terminal screen for better readability
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Print the column labels
    print("\n   a b c d e f g h")
    print("  +-----------------+")
    
    # Print each row of the board with the row labels
    board_rows = str(board).split("\n")
    for i, row in enumerate(board_rows):
        print(f"{8-i} | {row} | {8-i}")
    
    # Print the bottom border and column labels
    print("  +-----------------+")
    print("   a b c d e f g h")
    print("\n")

def get_move(board):
    """Prompts the player to input a valid move and validates it."""
    while True:
        # Prompt the player to enter their move
        move_input = input("\nEnter your move: ").strip()
        
        # Convert the input to lowercase for command processing
        command = move_input.lower()

        # Handle commands first
        if command in {"h", "help"}:
            display_help_menu()
            continue
        if command in {"i", "ins", "instructions"}:
            display_instructions()
            continue
        if command in {"undo", "u"}:
            # Undo the last move if there are moves to undo
            if len(board.move_stack) > 0:
                board.pop()
                print("\nLast move undone!\n")
                return None
            else:
                print("\nNo moves to undo!\n")
                continue
        if command in {"exit", "q", "e"}:
            # Exit the game gracefully
            print("\nGame exited. Thanks for playing!\n")
            exit(0)
        if command in {"c", "clear"}:
            # Clear the terminal and reprint the board
            os.system('cls' if os.name == 'nt' else 'clear')
            display_board(board)
            continue

        # Validate and process the move
        try:
            # Parse the move using the chess library's SAN parser
            move = board.parse_san(move_input)
            
            # Check if the move is legal
            if move in board.legal_moves:
                return move
            else:
                print("\nIllegal move! Try again.\n")
        except ValueError:
            # Handle invalid move input
            print("\nInvalid move! Use correct algebraic notation (e.g., e4, Nf3, O-O).\n")

def handle_promotion(board):
    """Handles the promotion of pawns when they reach the opposite end of the board."""
    # Check if the game is over before handling promotion
    if board.is_game_over():
        return
    
    # Get the last move made
    last_move = board.peek()
    
    # Get the destination square of the last move
    promotion_square = last_move.to_square
    
    # Check if a pawn has reached the opposite end of the board (promotion rank)
    if chess.square_rank(promotion_square) in {0, 7} and board.piece_type_at(promotion_square) == chess.PAWN:
        while True:
            # Prompt the player to choose a piece for promotion
            choice = input("\nPawn promotion! Choose (Q, R, B, N): ").upper()
            
            # Check if the chosen piece is valid
            if choice in {"Q", "R", "B", "N"}:
                # Map the choice to the corresponding piece type
                promotion_piece = {
                    "Q": chess.QUEEN,
                    "R": chess.ROOK,
                    "B": chess.BISHOP,
                    "N": chess.KNIGHT
                }[choice]
                
                # Remove the pawn from the promotion square
                board.remove_piece_at(promotion_square)
                
                # Place the chosen piece at the promotion square
                board.set_piece_at(promotion_square, chess.Piece(promotion_piece, board.turn))
                
                # Inform the player of the promotion
                print(f"\nPawn promoted to {choice}!\n")
                break
            else:
                print("\nInvalid choice! Please select Q, R, B, or N.\n")

def generate_pgn(board, white_player, black_player, result):
    """Generates a PGN (Portable Game Notation) formatted string representing the game."""
    # Define the event and date for the PGN header
    event = "Battle of Minds | Chess"
    date = datetime.datetime.now().strftime("%d.%m.%Y")
    termination = ""

    # Determine the termination reason based on the game outcome
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

    # Create the PGN header with event, date, players, and result
    pgn = f'[Event "{event}"]\n[Date "{date}"]\n[White "{white_player}"]\n'
    pgn += f'[Black "{black_player}"]\n[Result "{result}"]\n[Termination "{termination}"]\n\n'

    # Convert the move stack to SAN (Standard Algebraic Notation)
    moves = list(board.move_stack)
    san_moves = []
    temp_board = chess.Board()
    for move in moves:
        san_moves.append(temp_board.san(move))
        temp_board.push(move)

    # Format the moves into PGN format
    for i in range(0, len(san_moves), 2):
        pgn += f"{(i // 2) + 1}. {san_moves[i]}"
        if i + 1 < len(san_moves):
            pgn += f" {san_moves[i + 1]}"
        pgn += " "
    
    # Return the formatted PGN string
    return pgn.strip()

if __name__ == "__main__":
    main()