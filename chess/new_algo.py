class Piece:
    def __init__(self, color, position, piece_type, piece_status=0):
        self.color = color  # 1 -> white, 0 -> black
        self.position = position  # [row, col]
        self.type = piece_type
        self.status = piece_status  # 0 -> active, 1 -> captured

    def move(self, new_position):
        """Update piece position."""
        self.position = new_position

    def is_captured(self):
        """Mark piece as captured."""
        self.status = 1

    def __str__(self):
        """Unicode representation of the piece."""
        unicode_map = {
            'pawn': ('\u2659', '\u265f'),
            'rook': ('\u2656', '\u265c'),
            'knight': ('\u2658', '\u265e'),
            'bishop': ('\u2657', '\u265d'),
            'queen': ('\u2655', '\u265b'),
            'king': ('\u2654', '\u265a')
        }
        return unicode_map[self.type][self.color]

    def ascii_symbol(self):
        """Return ASCII representation of the piece."""
        return str(self)

    def possible_moves(self, board):
        """
        Base method for possible moves.
        Subclasses should override this.
        """
        return []

class Pawn(Piece):
    """Subclass for pawn"""
    def __init__(self, color, position, piece_type, piece_status=0):
        super().__init__(color, position, piece_type, piece_status)
        self.is_fresh = True

    def possible_moves(self, board):
        moves = []
        direction = -1 if self.color == 1 else 1
        row, col = self.position

        if board.get_piece_at([row + direction, col]) is None:
            moves.append([row + direction, col])

        if self.is_fresh and board.get_piece_at([row + 2 * direction, col]) is None:
            moves.append([row + 2 * direction, col])

        for dc in [-1, 1]:
            target = [row + direction, col + dc]
            target_piece = board.get_piece_at(target)
            if target_piece and target_piece.color != self.color:
                moves.append(target)

        return moves

    def move(self, new_position):
        """Override move to mark pawn as not fresh after the first move."""
        if self.is_fresh:
            self.is_fresh = False
        super().move(new_position)

class Rook(Piece):
    def possible_moves(self, board):
        moves = []
        row, col = self.position

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target = board.get_piece_at([r, c])
                if target is None:
                    moves.append([r, c])
                elif target.color != self.color:
                    moves.append([r, c])
                    break
                else:
                    break
                r, c = r + dr, c + dc

        return moves

class Knight(Piece):
    def possible_moves(self, board):
        moves = []
        row, col = self.position

        knight_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]

        for dr, dc in knight_moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = board.get_piece_at([r, c])
                if target is None or target.color != self.color:
                    moves.append([r, c])

        return moves

class Bishop(Piece):
    def possible_moves(self, board):
        moves = []
        row, col = self.position

        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target = board.get_piece_at([r, c])
                if target is None:
                    moves.append([r, c])
                elif target.color != self.color:
                    moves.append([r, c])
                    break
                else:
                    break
                r, c = r + dr, c + dc

        return moves

class Queen(Piece):
    def possible_moves(self, board):
        moves = []

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        row, col = self.position
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target = board.get_piece_at([r, c])
                if target is None:
                    moves.append([r, c])
                elif target.color != self.color:
                    moves.append([r, c])
                    break
                else:
                    break
                r, c = r + dr, c + dc

        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target = board.get_piece_at([r, c])
                if target is None:
                    moves.append([r, c])
                elif target.color != self.color:
                    moves.append([r, c])
                    break
                else:
                    break
                r, c = r + dr, c + dc

        return moves

class King(Piece):
    def possible_moves(self, board):
        moves = []
        row, col = self.position

        king_moves = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]

        for dr, dc in king_moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = board.get_piece_at([r, c])
                if target is None or target.color != self.color:
                    moves.append([r, c])

        return moves

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.pieces = []

    def setup_board(self):
        """Initialize the board with pieces."""
        for i in range(8):
            self.pieces.append(Pawn(1, [6, i], 'pawn'))
            self.pieces.append(Pawn(0, [1, i], 'pawn'))

        piece_classes = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for i, cls in enumerate(piece_classes):
            self.pieces.append(cls(1, [7, i], cls.__name__.lower()))
            self.pieces.append(cls(0, [0, i], cls.__name__.lower()))

        self.update_grid()

    def update_grid(self):
        """Update the board grid based on piece positions."""
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        for piece in self.pieces:
            if piece.status == 0:
                row, col = piece.position
                self.grid[row][col] = piece

    def display(self):
        """Print the board."""
        print("  a b c d e f g h")
        for i, row in enumerate(self.grid):
            print(8 - i, end=" ")
            for cell in row:
                if cell is None:
                    print('.', end=' ')
                else:
                    print(cell.ascii_symbol(), end=' ')
            print()
        print()

    def move_piece(self, start, end):
        """Move a piece from start to end position."""
        piece = self.get_piece_at(start)
        if piece:
            piece.move(end)
            self.update_grid()

    def get_piece_at(self, position):
        """Return the piece at a specific position."""
        row, col = position
        if 0<=row<8 and 0<=col<8:
            return self.grid[row][col]
        return None

    def __getitem__(self, index):
        """Make the board subscriptable."""
        return self.grid[index]

class ChessGame:
    def __init__(self):
        self.board = Board()
        self.board.setup_board()
        self.current_turn = 0  # 0 for white, 1 for black

    def display_board(self):
        print("\n  a b c d e f g h")
        print("  ----------------")
        for i in range(8):
            line = f"{8 - i} "
            for j in range(8):
                piece = self.board[i][j]
                if piece is None:
                    line += ". "
                else:
                    line += f"{piece.ascii_symbol()} "
            print(line)
        print("  ----------------")
        print("  a b c d e f g h\n")

    def get_player_input(self):
        while True:
            try:
                move = input("Enter your move (e.g. 'e2 e4'): ").strip()
                start, end = move.split()
                start_pos = [8 - int(start[1]), ord(start[0]) - ord('a')]
                end_pos = [8 - int(end[1]), ord(end[0]) - ord('a')]
                return start_pos, end_pos
            except ValueError:
                print("Invalid input. Please use the format 'e2 e4'.")

    def is_king_in_check(self, color):
        """Check if the king of the given color is in check."""
        for piece in self.board.pieces:
            if piece.type == 'king' and piece.color == color:
                king = piece
                break

        for piece in self.board.pieces:
            if piece.color != color and piece.type != 'king':
                if king.position in piece.possible_moves(self.board):
                    return True
        return False

    def has_legal_moves(self, color):
        """Check if the given player has any legal moves left."""
        for piece in self.board.pieces:
            if piece.color == color and piece.status == 0:
                for move in piece.possible_moves(self.board):
                    original_position = piece.position
                    piece.move(move)
                    if not self.is_king_in_check(color):
                        piece.move(original_position)
                        return True
                    piece.move(original_position)
        return False

    def is_game_over(self):
        """Check if the game is over due to checkmate, stalemate, or draw conditions."""
        if self.is_king_in_check(0) and not self.has_legal_moves(0):
            return "Checkmate! Black wins!"
        elif self.is_king_in_check(1) and not self.has_legal_moves(1):
            return "Checkmate! White wins!"
        elif not self.is_king_in_check(0) and not self.has_legal_moves(0):
            return "Stalemate! It's a draw."
        elif not self.is_king_in_check(1) and not self.has_legal_moves(1):
            return "Stalemate! It's a draw."
        else:
            return False

    def play_turn(self):
        self.display_board()
        print("White's turn" if self.current_turn == 0 else "Black's turn")

        start, end = self.get_player_input()

        piece = self.board.get_piece_at(start)
        if not piece or piece.color != self.current_turn:
            print("Invalid piece selection. Try again.")
            return False

        possible_moves = piece.possible_moves(self.board)
        if end not in possible_moves:
            print("Invalid move. Try again.")
            return False

        self.board.move_piece(start, end)
        self.current_turn = 1 - self.current_turn
        return True

    def play(self):
        print("Welcome to Super Chess")
        while not self.is_game_over():
            if not self.play_turn():
                continue
        print("Game Over!")


game = ChessGame()
game.play()
