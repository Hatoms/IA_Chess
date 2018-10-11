from PIL import Image, ImageTk
from chess_game import *

class Piece:

    def __init__(self,color,row,col,nbr,windows,nn):
        self.color = color
        self.row = row
        self.col = col
        self.nbr = nbr
        self.global_path = 'icons2/%s_%s.png'
        self.windows = windows
        self.nn = nn
        filename = self.global_path%(self.piece_name,self.color)
        self.tagname = "%s_%s_%d"%(self.piece_name,self.color,self.nbr)

        self.image = ImageTk.PhotoImage(file = filename, width=32, height=32)

        self.margin_left = 50
        self.margin_top = 50
        self.size_case = 60

    def create_piece(self):
        x = self.margin_left + self.col*self.size_case + self.size_case/2
        y = self.margin_top + self.row*self.size_case + self.size_case/2

        exec("%s = %s"%('self.windows.%s'%self.tagname,'self.image'))
        self.windows.create_image(x,y, image=self.image, tags=(self.tagname), anchor="c")

    def draw_piece(self):

        x = self.margin_left + self.col*self.size_case + self.size_case/2
        y = self.margin_top + self.row*self.size_case + self.size_case/2
        self.windows.create_image(x,y, image=self.image, tags=(self.tagname), anchor="c")

    def set_rowcol(self,row,col):
        self.row = row
        self.col = col


class Pawn(Piece):

    def __init__(self,color,row,col,nbr,windows):
        self.piece_name = 'pawn'
        self.has_moved = False
        Piece.__init__(self,color,row,col,nbr,windows,'p')

    def possible_cases(self,board,moves_white,moves_black,check):

        cases = []
        coef_color = -1 if self.color == "white" else 1

        if not board[self.row+(coef_color*1)][self.col]:
            if not self.has_moved:
                cases.append([self.row+(coef_color*1),self.col])
                if not board[self.row+(coef_color*2)][self.col]:
                    cases.append([self.row+(coef_color*2),self.col])
            else:
                cases.append([self.row+(coef_color*1),self.col])

        for i in [1,-1]:
            if self.col+i >= 0 and self.col+i <= 7:
                piece = board[self.row+(coef_color*1)][self.col+i]
                if piece and piece.color != self.color:
                    cases.append([self.row+(coef_color*1),self.col+i])
                if self.row == 3 and self.color == "white":
                    tmp = board[self.row][self.col+i]
                    if tmp and tmp.__class__.__name__ == "Pawn" and tmp.color != self.color:
                        last_move = moves_black[len(moves_black)-1]
                        if last_move[0] == 'p':
                            if last_move[1:] == ''.join(str(e) for e in [1,self.col+i,'o',3,self.col+i]):
                                cases.append([2,self.col+i])
                if self.row == 4 and self.color == "black":
                    tmp = board[self.row][self.col+i]
                    if tmp and tmp.__class__.__name__ == "Pawn" and tmp.color != self.color:
                         last_move = moves_white[len(moves_white)-1]
                         if last_move[0] == 'p':
                             if last_move[1:] == ''.join(str(e) for e in [6,self.col+i,'o',4,self.col+i]):
                                 cases.append([5,self.col+i])


        if check :
            chess = ChessGame()
            chess.tour = True if self.color == "black" else False
            ind_suppr = []
            for i in range(len(cases)) :

                c = cases[i]
                row_after,col_after = c
                temp1 = board[self.row][self.col]
                temp2 = board[row_after][col_after]
                board[self.row][self.col] = None
                board[row_after][col_after] = self
                if chess.is_check(board,moves_white,moves_black):
                    ind_suppr.append(i)
                board[self.row][self.col] = temp1
                board[row_after][col_after] = temp2

            cases = [x for i,x in enumerate(cases) if i not in ind_suppr]

        return cases





class Rook(Piece):

    def __init__(self,color,row,col,nbr,windows):
        self.piece_name = 'rook'
        Piece.__init__(self,color,row,col,nbr,windows,'r')

    def possible_cases(self,board,moves_white,moves_black,check):

        cases = []
        for coef in [[1,0],[-1,0],[0,1],[0,-1]]:
            i = 1
            while self.row + coef[0]*i < 8 and self.row + coef[0]*i > -1 and self.col+coef[1]*i < 8 and self.col+coef[1]*i > -1 :
                temp = board[self.row + coef[0]*i][self.col+coef[1]*i]
                if temp :
                    if temp.color == self.color :
                        break
                    else :
                        cases.append([self.row + coef[0]*i,self.col+coef[1]*i])
                        break
                else:
                    cases.append([self.row + coef[0]*i,self.col+coef[1]*i])
                i += 1

        if check :
            chess = ChessGame()
            chess.tour = True if self.color == "black" else False
            ind_suppr = []
            for i in range(len(cases)) :

                c = cases[i]
                row_after,col_after = c
                temp1 = board[self.row][self.col]
                temp2 = board[row_after][col_after]
                board[self.row][self.col] = None
                board[row_after][col_after] = self
                if chess.is_check(board,moves_white,moves_black):
                    ind_suppr.append(i)
                board[self.row][self.col] = temp1
                board[row_after][col_after] = temp2

            cases = [x for i,x in enumerate(cases) if i not in ind_suppr]

        return cases


class Bishop(Piece):

    def __init__(self,color,row,col,nbr,windows):
        self.piece_name = 'bishop'
        Piece.__init__(self,color,row,col,nbr,windows,'b')

    def possible_cases(self,board,moves_white,moves_black,check):

        cases = []
        for coef in [[1,1],[-1,-1],[1,-1],[-1,1]]:
            i = 1
            while self.row + coef[0]*i < 8 and self.row + coef[0]*i > -1 and self.col+coef[1]*i < 8 and self.col+coef[1]*i > -1 :
                temp = board[self.row + coef[0]*i][self.col+coef[1]*i]
                if temp :
                    if temp.color == self.color :
                        break
                    else :
                        cases.append([self.row + coef[0]*i,self.col+coef[1]*i])
                        break
                else:
                    cases.append([self.row + coef[0]*i,self.col+coef[1]*i])
                i += 1

        if check :
            chess = ChessGame()
            chess.tour = True if self.color == "black" else False
            ind_suppr = []
            for i in range(len(cases)) :

                c = cases[i]
                row_after,col_after = c
                temp1 = board[self.row][self.col]
                temp2 = board[row_after][col_after]
                board[self.row][self.col] = None
                board[row_after][col_after] = self
                if chess.is_check(board,moves_white,moves_black):
                    ind_suppr.append(i)
                board[self.row][self.col] = temp1
                board[row_after][col_after] = temp2

            cases = [x for i,x in enumerate(cases) if i not in ind_suppr]

        return cases

class Knight(Piece):

    def __init__(self,color,row,col,nbr,windows):
        self.piece_name = 'knight'
        Piece.__init__(self,color,row,col,nbr,windows,'k')

    def possible_cases(self,board,moves_white,moves_black,check):

        cases = []
        for coef in [[2,1],[2,-1],[-2,1],[-2,-1],[1,2],[-1,2],[1,-2],[-1,-2]]:
            new_row = self.row + coef[0]
            new_col = self.col + coef[1]

            if new_row < 0 or new_row > 7 or new_col < 0 or new_col > 7:
                continue
            piece = board[new_row][new_col]
            if piece and piece.color == self.color :
                continue
            else :
                cases.append([new_row,new_col])

        if check :
            chess = ChessGame()
            chess.tour = True if self.color == "black" else False
            ind_suppr = []
            for i in range(len(cases)) :

                c = cases[i]
                row_after,col_after = c
                temp1 = board[self.row][self.col]
                temp2 = board[row_after][col_after]
                board[self.row][self.col] = None
                board[row_after][col_after] = self
                if chess.is_check(board,moves_white,moves_black):
                    ind_suppr.append(i)
                board[self.row][self.col] = temp1
                board[row_after][col_after] = temp2

            cases = [x for i,x in enumerate(cases) if i not in ind_suppr]

        return cases





class Queen(Piece):

    def __init__(self,color,row,col,nbr,windows):
        self.piece_name = 'queen'
        Piece.__init__(self,color,row,col,nbr,windows,'q')

    def possible_cases(self,board,moves_white,moves_black,check):

        cases = []
        for coef in [[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,-1],[1,-1],[-1,1]]:
            i = 1
            while self.row + coef[0]*i < 8 and self.row + coef[0]*i > -1 and self.col+coef[1]*i < 8 and self.col+coef[1]*i > -1 :
                temp = board[self.row + coef[0]*i][self.col+coef[1]*i]
                if temp :
                    if temp.color == self.color :
                        break
                    else :
                        cases.append([self.row + coef[0]*i,self.col+coef[1]*i])
                        break
                else:
                    cases.append([self.row + coef[0]*i,self.col+coef[1]*i])
                i += 1

        if check :
            chess = ChessGame()
            chess.tour = True if self.color == "black" else False
            ind_suppr = []
            for i in range(len(cases)) :

                c = cases[i]
                row_after,col_after = c
                temp1 = board[self.row][self.col]
                temp2 = board[row_after][col_after]
                board[self.row][self.col] = None
                board[row_after][col_after] = self
                if chess.is_check(board,moves_white,moves_black):
                    ind_suppr.append(i)
                board[self.row][self.col] = temp1
                board[row_after][col_after] = temp2

            cases = [x for i,x in enumerate(cases) if i not in ind_suppr]

        return cases

class King(Piece):

    def __init__(self,color,row,col,nbr,windows):
        self.piece_name = 'king'
        Piece.__init__(self,color,row,col,nbr,windows,'K')

    def possible_cases(self,board,moves_white,moves_black,check):

        cases = []
        for coef in [[0,1],[0,-1],[1,0],[-1,0],[1,1],[-1,1],[1,-1],[-1,-1]]:
            new_row = self.row + coef[0]
            new_col = self.col + coef[1]

            if new_row < 0 or new_row > 7 or new_col < 0 or new_col > 7:
                continue
            piece = board[new_row][new_col]
            if piece and piece.color == self.color :
                continue
            else :
                cases.append([new_row,new_col])

        cases += self.castling(board,moves_white,moves_black)
        chess = ChessGame()
        chess.tour = True if self.color == "black" else False
        ind_suppr = []
        for i in range(len(cases)) :

            c = cases[i]
            row_after,col_after = c
            temp1 = board[self.row][self.col]
            temp2 = board[row_after][col_after]
            board[self.row][self.col] = None
            board[row_after][col_after] = self
            if chess.is_check(board,moves_white,moves_black) or self.is_next_to_king(board,row_after,col_after):
                ind_suppr.append(i)
            board[self.row][self.col] = temp1
            board[row_after][col_after] = temp2

        cases = [x for i,x in enumerate(cases) if i not in ind_suppr]

        return cases

    def is_next_to_king(self,board,row,col):

        for coef in [[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,-1],[1,-1],[-1,1]]:

            new_row = row + coef[0]
            new_col = col + coef[1]

            if new_row >= 0 and new_row <= 7 and new_col >= 0 and new_col <= 7:
                if board[new_row][new_col].__class__.__name__ == "King":
                    return True

        return False

    def castling(self,board,moves_white,moves_black):

        moves = moves_white if self.color == "white" else moves_black
        fr = 7 if self.color == "white" else 0
        cases = []
        if self.row != fr or self.col != 4:
            return []

        for rock in [0,7]:
            have_to_continu = False
            if not board[fr][rock] or board[fr][rock].color != self.color or board[fr][rock].__class__.__name__ != "Rook":
                continue

            for colone in self.get_between(rock,self.col):
                if board[fr][colone]:
                    have_to_continu = True
                    break
                chess = ChessGame()
                chess.tour = True if self.color == "black" else False
                if colone != rock:

                    row_after,col_after = fr,colone
                    temp1 = board[self.row][self.col]
                    temp2 = board[row_after][col_after]
                    board[self.row][self.col] = None
                    board[row_after][col_after] = self
                    if chess.is_check(board,moves_white,moves_black):
                        board[self.row][self.col] = temp1
                        board[row_after][col_after] = temp2
                        have_to_continu = False
                        break
                    board[self.row][self.col] = temp1
                    board[row_after][col_after] = temp2



            if not have_to_continu:
                for m in reversed(moves):
                    if m[0] == 'K' or m[0:3]=='r'+str(fr)+str(rock):
                        have_to_continu = False
                        return []

            if have_to_continu:
                continue

            castl = 6 if rock == 7 else 2
            cases.append([fr,castl])

        return cases



    def get_between(self,a,b):
        if  a < b :
            return range(a+1,b)

        return range(b+1,a)
