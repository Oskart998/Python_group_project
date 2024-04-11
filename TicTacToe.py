class TicTacToe:
    def __init__(self):
        # Initialize the game by resetting the board
        self.reset()

    def reset(self):
        # Reset the board to an empty state
        self.board = [[' ']*3 for _ in range(3)]
        # Set the current player to 'X' to start the game
        self.current_player = 'X'

    def make_move(self, row, col):
        # Check if the chosen cell is empty
        if self.board[row][col] == ' ':
            # Place the current player's mark on the chosen cell
            self.board[row][col] = self.current_player
            # Switch to the other player for the next turn
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            # Move successful
            return True
        # Move not possible, cell already occupied
        return False

    def check_winner(self):
        # Check rows for a win
        for row in self.board:
            if row[0] == row[1] == row[2] != ' ':
                return row[0]

        # Check columns for a win
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != ' ':
                return self.board[0][col]

        # Check diagonals for a win
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]

        # If the board is full but no winner, it's a draw
        if all(cell != ' ' for row in self.board for cell in row):
            return 'Draw'

        # No winner yet
        return None

    def is_board_full(self):
        # Check if all cells on the board are occupied
        return all(cell != ' ' for row in self.board for cell in row)
