class ChessGame:

    def __init__(self):
        self.tour = True
        self.is_selected = False
        self.check = False
        self.board_white_memory = []
        self.b_w_m = []
        self.board_black_memory = []
        self.b_b_m = []
        self.draw_message = ""

    def is_check(self,board,moves_white,moves_black):
        color_tour = "white" if self.tour else "black"
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and piece.__class__.__name__ != "King" and piece.color == color_tour :
                    cases = piece.possible_cases(board,moves_white,moves_black,self.check)
                    for case in cases :
                        if board[case[0]][case[1]].__class__.__name__ == "King":
                            self.check = True
                            return self.check

        self.check = False
        return self.check

    def is_checkmate(self,board,moves_white,moves_black):
        if not self.check :
            return False
        else :
            color_tour = "white" if self.tour else "black"
            for row in range(8):
                for col in range(8):
                    piece = board[row][col]
                    if piece and piece.color != color_tour :
                        cases = piece.possible_cases(board,moves_white,moves_black,self.check)
                        for c in cases :
                            row_after,col_after = c
                            temp1 = board[row][col]
                            temp2 = board[row_after][col_after]
                            board[row][col] = None
                            board[row_after][col_after] = piece
                            if not self.is_check(board,moves_white,moves_black):
                                board[row][col] = temp1
                                board[row_after][col_after] = temp2
                                self.check = True
                                return False
                            board[row][col] = temp1
                            board[row_after][col_after] = temp2


        return True

    def is_pat(self,board,moves_white,moves_black):
        color_tour = "white" if self.tour else "black"
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and piece.color != color_tour :
                    cases = piece.possible_cases(board,moves_white,moves_black,self.check)
                    if len(cases)>0:
                        return False

        return True

    def nothing_happen(self,moves_white,moves_black):


            for i in range(1,26):
                if len(moves_white) >= i and len(moves_black) >= i:
                    w = moves_white[len(moves_white)-i]
                    b = moves_black[len(moves_black)-i]
                    if w[0] == 'p' or b[0] =='p' or w[3] == 'x' or b[3] == 'x':
                        return False
                else:
                    return False
            return True

    def insufficient_material(self,board):

        forbid = ["Pawn","Rook","Queen"]
        one_bishop = False

        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and piece.color == "white":
                    if piece.__class__.__name__ in forbid:
                        return False
                    elif piece.__class__.__name__ == "Knight":
                        forbid.append("Knight")
                    elif piece.__class__.__name__ == "Bishop" and not one_bishop:
                        forbid.append("Bishop")
                        one_bishop = True
                        col_bishop = ((row+col)%2 == 0)

        one_bishop = False
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and piece.color == "black":
                    if piece.__class__.__name__ in forbid:
                        if piece.__class__.__name__ == "Bishop" and not one_bishop:
                            if ((row+col)%2 == 0) != col_bishop:
                                return False
                            one_bishop = True
                        else:
                            return False

        return True

    def board_to_string(self,board):

        str = ""
        for row in board:
            for elem in row:
                if not elem:
                    str += " "
                else:
                    piece = elem.__class__.__name__
                    if piece == "Pawn":
                        str += "p"
                    elif piece == "Rook":
                        str += "r"
                    elif piece == "Knight":
                        str += "k"
                    elif piece == "Bishop":
                        str += "b"
                    elif piece == "Queen":
                        str += "Q"
                    else:
                        str += "K"
            str += '\n'
        return str

    def same_board(self,board,moves_white,moves_black):

        brd = self.board_to_string(board)
        moves = moves_white if self.tour else moves_black

        if moves[len(moves)-1][3] == "x":
            self.board_white_memory = []
            self.b_w_m = []
            self.board_black_memory = []
            self.b_b_m = []
            return False


        if self.tour:
            if brd not in self.board_white_memory :
                self.board_white_memory.insert(0,brd)
                self.b_w_m.insert(0,1)
                return False
            else:
                if self.b_w_m[self.board_white_memory.index(brd)] < 3:
                    self.b_w_m[self.board_white_memory.index(brd)] += 1
                    return False

        else:
            if brd not in self.board_black_memory :
                self.board_black_memory.insert(0,brd)
                self.b_b_m.insert(0,1)
                return False
            else:
                if self.b_b_m[self.board_black_memory.index(brd)] < 3:
                    self.b_b_m[self.board_black_memory.index(brd)] += 1
                    return False

        return True

    def is_draw(self,board,moves_white,moves_black):

        if self.is_pat(board,moves_white,moves_black):
            self.draw_message = "PAT"
            return True

        if self.insufficient_material(board):
            self.draw_message = "insufficient_material"
            return True

        if self.nothing_happen(moves_white,moves_black):
            self.draw_message = "50 moves without prises"
            return True

        if self.same_board(board,moves_white,moves_black):
            self.draw_message = "3 posistions identiques"
            return True
