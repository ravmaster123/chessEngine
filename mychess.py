import copy
class Piece:
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.symbol = None
    def check_path_clear(self, new_pos, board):
        row, col = self.position
        new_row, new_col = new_pos
        if board.is_piece_at(new_row, new_col) and board.get_piece_color_at(new_row, new_col) == self.color:
            return False
        if row == new_row:
            if col < new_col:
                for i in range(col + 1, new_col):
                    if board.is_piece_at(row, i):
                        return False
            else:
                for i in range(new_col + 1, col):
                    if board.is_piece_at(row, i):
                        return False
        elif col == new_col:
            if row < new_row:
                for i in range(row + 1, new_row):
                    if board.is_piece_at(i, col):
                        return False
            else:
                for i in range(new_row + 1, row):
                    if board.is_piece_at(i, col):
                        return False
        elif abs(row - new_row) == abs(col - new_col):
            if row < new_row and col < new_col:
                for i in range(1, abs(row - new_row)):
                    if board.is_piece_at(row + i, col + i):
                        return False
            elif row < new_row and col > new_col:
                for i in range(1, abs(row - new_row)):
                    if board.is_piece_at(row + i, col - i):
                        return False
            elif row > new_row and col < new_col:
                for i in range(1, abs(row - new_row)):
                    if board.is_piece_at(row - i, col + i):
                        return False
            elif row > new_row and col > new_col:
                for i in range(1, abs(row - new_row)):
                    if board.is_piece_at(row - i, col - i):
                        return False
        return True
    def check_king_open(self, new_pos, board):
        temp_board = copy.deepcopy(board)
        otherBoardPiece = temp_board.get_piece_at(*self.position)
        otherBoardPiece.move(new_pos, temp_board)
        if temp_board.is_king_under_attack(self.color):
            return False
        return True

    def boardMistake(self, new_pos, board):
        return self.check_king_open(self, new_pos, board) and self.check_path_clear(self, new_pos, board)
    def move(self, new_pos, board):

        board.set_piece_at(None, *self.position)
        board.set_piece_at(self, *new_pos)
        self.position = new_pos
        return True

class King(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        if self.color == "white":
            self.symbol = 'K'
        else:
            self.symbol = 'k'
        self.hasMoved = False

    def is_valid_move(self, new_pos, board):
        # Check if new position is on the same row, column or diagonal
        row, col = self.position
        new_row, new_col = new_pos
        row_diff = (new_row - row)
        col_diff = (new_col - col)
        if abs(row_diff) <= 1 and abs(col_diff) <= 1:
            return self.check_path_clear(new_pos, board)
        if not self.hasMoved and abs(col_diff) == 2 and row_diff == 0:
            if row_diff == 0 and col_diff == 2:
                sldRook = board.get_piece_at(row, 7)
            elif row_diff == 0 and col_diff == -2:
                sldRook = board.get_piece_at(row, 0)
            if type(sldRook) == Rook and sldRook.color == self.color and sldRook.hasMoved == False:
                if not board.is_king_under_attack(self.color):
                    temp_boardOne = copy.deepcopy(board)
                    otherBoardPieceOne = temp_boardOne.get_piece_at(*self.position)
                    otherBoardPieceOne.move((self.position[0], self.position[1] + col_diff//2), temp_boardOne)
                    temp_boardTwo = copy.deepcopy(board)
                    otherBoardPieceTwo = temp_boardTwo.get_piece_at(*self.position)
                    otherBoardPieceTwo.move((self.position[0], self.position[1] + col_diff), temp_boardTwo)
                    if not temp_boardOne.is_king_under_attack(self.color) and not temp_boardTwo.is_king_under_attack(self.color):
                        if self.check_path_clear((sldRook.position[0], sldRook.position[1] - col_diff//2), board):
                            board.castle(sldRook, (self.position[0], self.position[1] + col_diff//2))
                            return True
        return False

class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        if self.color == "white":
            self.symbol = 'R'
        else:
            self.symbol = 'r'
        self.hasMoved = False

    def is_valid_move(self, new_pos, board):
        # Check if new position is on the same row or column
        row, col = self.position
        new_row, new_col = new_pos
        if new_row == row or new_col == col:
            return self.check_path_clear(new_pos, board)
        return False

class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        if self.color == "white":
            self.symbol = 'N'
        else:
            self.symbol = 'n'

    def is_valid_move(self, new_pos, board):
        # Check if new position is a valid L-shape from current position
        row, col = self.position
        new_row, new_col = new_pos
        row_diff = abs(new_row - row)
        col_diff = abs(new_col - col)
        if board.is_piece_at(new_row, new_col) and board.get_piece_color_at(new_row, new_col) == self.color:
            return False
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)


class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        if self.color == "white":
            self.symbol = 'B'
        else:
            self.symbol = 'b'

    def is_valid_move(self, new_pos, board):
        # Check if new position is on the same diagonal
        row, col = self.position
        new_row, new_col = new_pos
        row_diff = abs(new_row - row)
        col_diff = abs(new_col - col)
        if row_diff == col_diff:
            return self.check_path_clear(new_pos, board)
        return False


class Queen(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        if self.color == "white":
            self.symbol = 'Q'
        else:
            self.symbol = 'q'

    def is_valid_move(self, new_pos, board):
        # Check if new position is on the same row, column or diagonal
        row, col = self.position
        new_row, new_col = new_pos
        row_diff = abs(new_row - row)
        col_diff = abs(new_col - col)
        if new_row == row or new_col == col:
            return self.check_path_clear(new_pos, board)
        elif row_diff == col_diff:
            return self.check_path_clear(new_pos, board)
        return False

class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        if self.color == "white":
            self.symbol = 'P'
        else:
            self.symbol = 'p'

    def is_valid_move(self, new_pos, board):
        row, col = self.position
        new_row, new_col = new_pos
        row_diff = new_row - row
        col_diff = new_col - col
        if (self.color == 'white' and row_diff == 1) or (self.color == 'black' and row_diff == -1):
            if abs(col_diff) == 1:
                if board.is_piece_at(*new_pos) and board.get_piece_color_at(*new_pos) != self.color:
                    return True
                if board.forcedMove[0]:
                    if row == board.forcedMove[1][0] and abs(col - board.forcedMove[1][1]) == 1:
                        if (self.color == 'white' and new_row == board.forcedMove[1][0]+1 and new_col == board.forcedMove[1][1]) or (self.color == 'black' and new_row == board.forcedMove[1][0] - 1 and new_col == board.forcedMove[1][1]):
                            board.set_piece_at(None, *board.forcedMove[1])
                            return True
            elif abs(col_diff) == 0:
                return self.check_path_clear(new_pos, board)
        if abs(row_diff) == 2 and col_diff == 0 and ((self.color == 'white' and row == 1) or (self.color == 'black' and row == 6)):
            if board.is_piece_at(new_row, new_col) and board.get_piece_color_at(new_row, new_col) != self.color:
                return False
            return self.check_path_clear(new_pos, board)
        return False

class ChessBoard:
    def __init__(self):
        self.board = [[None for j in range(8)] for i in range(8)]
        self.setup_board()
        self.forcedMove = [False, (0, 0)]
        self.turn = "white"
        self.checkOrMate = {"white": [False, False, False], "black": [False, False, False]} #Check, Stale, Mate

    def set_piece_at(self, piece, row, col):
        self.board[row][col] = piece
        if piece:
            piece.position = (row, col)

    def promote(self, piece, row, col):
        if piece == "R":
            self.board.set_piece_at(Rook(self.turn, (row, col)), row, col)
        if piece == "N":
            self.board.set_piece_at(Knight(self.turn, (row, col)), row, col)
        if piece == "B":
            self.board.set_piece_at(Bishop(self.turn, (row, col)), row, col)
        if piece == "Q":
            self.board.set_piece_at(Queen(self.turn, (row, col)), row, col)

    def get_piece_at(self, row, col):
        return self.board[row][col]

    def is_piece_at(self, row, col):
        return self.board[row][col] is not None

    def makeMoveStraight(self, moveTuple):
        #This function only for machine use (skips all move validity checks)
        toMove = self.get_piece_at(moveTuple[0], moveTuple[1])
        #En Passant
        if type(toMove) == Pawn and abs(moveTuple[2] - moveTuple[0]) == 2:
            self.forcedMove = (True, (moveTuple[2], moveTuple[3]))
        else:
            self.forcedMove = (False, (0, 0))
        toMove.move((moveTuple[2], moveTuple[3]), self)
        #Promotion
        if type(toMove) == Pawn and moveTuple[2] == 7 or moveTuple[2] == 0:
            self.promote(moveTuple[4], moveTuple[2], moveTuple[3])

        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"
        if self.is_king_under_attack(self.turn):
            self.checkOrMate[self.turn][0] = True
            print("CHECK")
            if len(self.legal_moves()[0]) == 0:
                print("CHECKMATE")
                self.checkOrMate[self.turn][2] = True
            else:
                self.checkOrMate[self.turn][2] = False
        else:
            self.checkOrMate[self.turn][0] = False
            if len(self.legal_moves()[0]) == 0:
                print("STALEMATE")
                self.checkOrMate[self.turn][1] = True
            else:
                self.checkOrMate[self.turn][1] = False
        return self.checkOrMate

    def get_piece_color_at(self, row, col):
        return self.board[row][col].color
    def castle(self, rook, new_pos):
        self.set_piece_at(Rook(rook.color, new_pos), *new_pos)
        self.set_piece_at(None, *rook.position)
        return
    def legal_moves(self):
        x=[]
        for row in range(8):
            for col in range(8):
                if self.is_piece_at(row, col) and self.get_piece_color_at(row, col) == self.turn:
                    for rowrow in range(8):
                        for colcol in range(8):
                            if (self.get_piece_at(row, col).is_valid_move((rowrow, colcol), self) and self.get_piece_at(row, col).check_king_open((rowrow, colcol), self)):
                                if type(self.get_piece_at(row, col)) == Pawn and (rowrow == 7 or rowrow == 0):
                                    x.append((row, col, rowrow, colcol, "R"))
                                    x.append((row, col, rowrow, colcol, "N"))
                                    x.append((row, col, rowrow, colcol, "B"))
                                    x.append((row, col, rowrow, colcol, "Q"))
                                else:
                                    x.append((row, col, rowrow, colcol))
        return (x, len(x))
    def is_king_under_attack(self, king_color):
        # Find the position of the king
        for row in range(8):
            for col in range(8):
                piece = self.get_piece_at(row, col)
                if isinstance(piece, King) and piece.color == king_color:
                    king_pos = (row, col)
                    break
            else:
                continue
            break

        # Check if any opponent's piece can move to the king's position
        for row in range(8):
            for col in range(8):
                piece = self.get_piece_at(row, col)
                if piece and piece.color != king_color:
                    if piece.is_valid_move(king_pos, self) and piece.check_path_clear(king_pos, self):
                        return True

        return False

    def print_board(self):
        for row in self.board[::-1]:
            print(self.board.index(row), end = ' ')
            for piece in row:
                if piece is None:
                    print('.', end=' ')
                else:
                    print(piece.symbol, end=' ')
            print()
        print('  0 1 2 3 4 5 6 7')
    def getState(self):
        state = (self.board, self.turn, self.forcedMove, self.checkOrMate)
        return state
    def setup_board(self):
        self.set_piece_at(Rook('white', (0, 0)), 0, 0)
        self.set_piece_at(Knight('white', (0, 1)), 0, 1)
        self.set_piece_at(Bishop('white', (0, 2)), 0, 2)
        self.set_piece_at(Queen('white', (0, 3)), 0, 3)
        self.set_piece_at(King('white', (0, 4)), 0, 4)
        self.set_piece_at(Bishop('white', (0, 5)), 0, 5)
        self.set_piece_at(Knight('white', (0, 6)), 0, 6)
        self.set_piece_at(Rook('white', (0, 7)), 0, 7)

        for col in range(8):
            self.set_piece_at(Pawn('white', (1, col)), 1, col)
        # Set up black pieces
        self.set_piece_at(Rook('black', (7, 0)), 7, 0)
        self.set_piece_at(Knight('black', (7, 1)), 7, 1)
        self.set_piece_at(Bishop('black', (7, 2)), 7, 2)
        self.set_piece_at(Queen('black', (7, 3)), 7, 3)
        self.set_piece_at(King('black', (7, 4)), 7, 4)
        self.set_piece_at(Bishop('black', (7, 5)), 7, 5)
        self.set_piece_at(Knight('black', (7, 6)), 7, 6)
        self.set_piece_at(Rook('black', (7, 7)), 7, 7)
        for col in range(8):
            self.set_piece_at(Pawn('black', (6, col)), 6, col)
def forHuman():
    board = ChessBoard()  # Initialize the board
    board.print_board()
    while True:
        # Handling valid input for piece
        while True:
            try:
                row = int(input("Row (0-7): "))
                if row < 0 or row > 7:
                    raise ValueError("Row must be an integer between 0 and 7.")

                column = int(input("Column (0-7): "))
                if column < 0 or column > 7:
                    raise ValueError("Column must be an integer between 0 and 7.")

                if not board.is_piece_at(row, column):
                    raise ValueError("Please select a piece")

                if board.get_piece_color_at(row, column) != board.turn:
                    raise ValueError("Please select a " + board.turn + " piece")
                break
            except ValueError as ve:
                if "Row" in str(ve):
                    print(f"Invalid row input: {ve}")
                elif "Column" in str(ve):
                    print(f"Invalid column input: {ve}")
                else:
                    print(f"Invalid input: {ve}")
        # Get selected piece
        toMove = board.get_piece_at(row, column)
        # Handling valid input for new position
        while True:
            try:
                rowy = (input("New Row (0-7) or r to reselect: "))
                if rowy == "r":
                    print("ajds kasdj ")
                    break
                new_row = int(rowy)
                if new_row < 0 or new_row > 7:
                    raise ValueError("New Row must be an integer between 0 and 7.")

                new_column = int(input("New Column (0-7): "))
                if new_column < 0 or new_column > 7:
                    raise ValueError("New Column must be an integer between 0 and 7.")

                if not (toMove.is_valid_move((new_row, new_column), board) and toMove.check_king_open(
                        (new_row, new_column), board)):
                    raise ValueError("Illegal Move")
                break
            except ValueError as ve:
                if "Row" in str(ve):
                    print(f"Invalid row input: {ve}")
                elif "Column" in str(ve):
                    print(f"Invalid column input: {ve}")
                elif "Illegal" in str(ve):
                    print(f"Bruh: {ve}")
                else:
                    print(f"Invalid input: {ve}")

        # Handle en passant case
        if type(toMove) == Pawn and abs(new_row - row) == 2:
            board.forcedMove = (True, (new_row, new_column))
        else:
            board.forcedMove = (False, (0, 0))
        toMove.move((new_row, new_column), board)
        # Promotion
        if type(toMove) == Pawn and new_row == 7 or new_row == 0:
            while True:
                try:
                    promPiece = input("Enter R, N, B, Q: ")
                    if promPiece not in ("R", "N", "B", "Q"):
                        raise ValueError("Type R, N, B or Q: ")
                    break
                except ValueError as ve:
                    print("Reenter piece to be promoted to")
            board.promote(promPiece, new_row, new_column)
        if type(toMove) == King or type(toMove) == Rook:
            toMove.hasMoved = True
        board.print_board()
        if board.turn == "white":
            board.turn = "black"
        else:
            board.turn = "white"
        #print(board.legal_moves())
        if board.is_king_under_attack(board.turn):
            board.checkOrMate[board.turn][0] = True
            print("CHECK")
            if len(board.legal_moves()[0]) == 0:
                print("CHECKMATE")
                board.checkOrMate[board.turn][2] = True
            else:
                board.checkOrMate[board.turn][2] = False
        else:
            board.checkOrMate[board.turn][0] = False
            if len(board.legal_moves()[0]) == 0:
                print("STALEMATE")
                board.checkOrMate[board.turn][1] = True
            else:
                board.checkOrMate[board.turn][1] = False
        if board.checkOrMate[board.turn][1] or board.checkOrMate[board.turn][2]:
            break
def forMachine():
    board = ChessBoard()  # Initialize the board
    board.setup_board()
    while True:
        outcome = board.makeMoveStraight(input())
        if outcome[1] or outcome[4]:
            return "draw"
        elif outcome[2]:
            return "black"
        elif outcome[5]:
            return "white"

if __name__ == '__main__':
    forHuman()
