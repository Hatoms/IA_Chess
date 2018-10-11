from Tkinter import *


from piece import *
from chess_game import *

class Board:

    def __init__(self,size_windows,margin_left,margin_top,size_case,root):

        # filenames = {}
        # filenames["pawn"] = ('icons/pawn_white.png','icons/pawn_black.png')
        # filenames["bishop"] = ('icons/bishop_white.png','icons/bishop_black.png')
        # filenames["rook"] = ('icons/rook_white.png','icons/rook_black.png')
        # filenames["knight"] = ('icons/knight_white.png','icons/knight_black.png')
        # filenames["queen"] = ('icons/queen_white.png','icons/queen_black.png')
        # # filenames["king"] = ('icons/king_white.png','icons/king_black.png')
        # filenames["king"] = ('icons/chess-17-64.png','icons/king_black.png')

        self.board = [[None for x in range(8)] for y in range(8)]
        self.moves_white = []
        self.moves_black = []
        self.windows = Canvas(width = size_windows, height = size_windows, bg = "grey")
        self.windows.pack()
        self.color_even = "orange"
        self.color_odd = "green"
        self.color_even_selected = "yellow"
        self.color_odd_selected = "lawn green"
        self.color_taken = "red"

        self.margin_left = margin_left
        self.margin_top = margin_top
        self.size_case = size_case
        self.root = root



        for col in range(8):
            for row in range(8):
                self.draw_rectangle(row,col)

        self.board[0][0] = Rook("black",0,0,1,self.windows)
        self.board[0][1] = Knight("black",0,1,1,self.windows)
        self.board[0][2] = Bishop("black",0,2,1,self.windows)
        self.board[0][3] = Queen("black",0,3,1,self.windows)
        self.board[0][4] = King("black",0,4,1,self.windows)
        self.board[0][5] = Bishop("black",0,5,2,self.windows)
        self.board[0][6] = Knight("black",0,6,2,self.windows)
        self.board[0][7] = Rook("black",0,7,2,self.windows)
        for i in range(8):
            self.board[1][i] = Pawn("black",1,i,i+1,self.windows)

        self.board[7][0] = Rook("white",7,0,1,self.windows)
        self.board[7][1] = Knight("white",7,1,1,self.windows)
        self.board[7][2] = Bishop("white",7,2,1,self.windows)
        self.board[7][3] = Queen("white",7,3,1,self.windows)
        self.board[7][4] = King("white",7,4,1,self.windows)
        self.board[7][5] = Bishop("white",7,5,2,self.windows)
        self.board[7][6] = Knight("white",7,6,2,self.windows)
        self.board[7][7] = Rook("white",7,7,2,self.windows)
        for i in range(8):
            self.board[6][i] = Pawn("white",6,i,i+1,self.windows)

        for row in self.board:
            for piece in row:
                if piece :
                    piece.create_piece()

        self.selected = []

    def draw_rectangle(self,row,col,selected = False, taken = False):

        x_temp = self.margin_left + col*self.size_case
        y_temp = self.margin_top + row*self.size_case
        if selected:
            if taken:
                color_temp = self.color_taken
            else:

                color_temp = self.color_even_selected if (row+col)%2 == 0 else self.color_odd_selected

        else:
            color_temp = self.color_even if (row+col)%2 == 0 else self.color_odd

        self.windows.create_rectangle(x_temp,y_temp,x_temp+self.size_case,y_temp+self.size_case, fill = color_temp)


    def draw_check(self,tour,unselect = False):
        color_tour = "white" if tour else "black"
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color != color_tour and piece.__class__.__name__ == "King":
                    if unselect:
                        self.draw_rectangle(row,col)
                    else:
                        self.draw_rectangle(row,col,True,True)
                    piece.draw_piece()
                    return 0


    def find_case(self,x,y):

        for x_temp in range(50,480,60):
            if x > x_temp and x < x_temp+self.size_case:
                col = ((x_temp+10)/60)-1
                for y_temp in range(50,480,60):
                    if y > y_temp and y < y_temp+self.size_case:
                        row = ((y_temp+10)/60)-1
                        return(row,col)

        return None


    def piece_selected(self,x,y,tour,check):
        case_temp = self.find_case(x,y)
        color_temp = "white" if tour else "black"
        if case_temp:
            row,col = case_temp
            temp_piece = self.board[row][col]
            if temp_piece and temp_piece.color == color_temp:

                self.draw_rectangle(row,col,True)
                temp_piece.draw_piece()
                self.selected.append([temp_piece,[row,col]])

                cases = temp_piece.possible_cases(self.board,self.moves_white,self.moves_black,check)

                for c in cases:
                    self.selected.append(c)
                    row,col = c
                    piece_taken = self.board[row][col]
                    if piece_taken:
                        self.draw_rectangle(row,col,True,True)
                        piece_taken.draw_piece()
                    else:
                        self.draw_rectangle(row,col,True)

                self.is_selected = True

                return True

        return False

    def print_board(self):

        print "-----------------------------"
        for row in self.board:
            temp = ""
            for elem in row:
                if not elem:
                    temp += " "
                else:
                    piece = elem.__class__.__name__
                    if piece == "Pawn":
                        temp += "p"
                    elif piece == "Rook":
                        temp += "r"
                    elif piece == "Knight":
                        temp += "k"
                    elif piece == "Bishop":
                        temp += "b"
                    elif piece == "Queen":
                        temp += "Q"
                    else:
                        temp += "K"

            print temp
        print "-----------------------------"


    def case_unselect(self):

        if len(self.selected) > 0:
            piece_selected = self.selected.pop(0)
            temp_piece = piece_selected[0]
            row,col = piece_selected[1]

            self.draw_rectangle(row,col)
            temp_piece.draw_piece()

        for cases in self.selected:
            self.draw_rectangle(cases[0],cases[1])
            piece = self.board[cases[0]][cases[1]]
            if piece :
                piece.draw_piece()

        self.is_selected = False

        self.selected = []

    def try_moving(self,x,y,check,tour):

        case_temp = self.find_case(x,y)
        if case_temp:
            case_temp = list(case_temp)
            if case_temp in self.selected:

                self.move(case_temp,tour)
                if check:
                    self.draw_check(tour,True)
                return True


        self.case_unselect()
        return False

    def queek_move(self,temp_piece,case_temp,check,tour):

        self.selected.append([temp_piece,[temp_piece.row,temp_piece.col]])
        self.move(case_temp,tour)
        if check:
            self.draw_check(tour,True)


    def move(self,case_temp,tour):

        temp_piece = self.selected[0][0]
        move_name = temp_piece.nn + ''.join(str(e) for e in self.selected[0][1])
        temp_piece.set_rowcol(case_temp[0],case_temp[1])

        self.board[self.selected[0][1][0]][self.selected[0][1][1]] = None
        if temp_piece.__class__.__name__ == "Pawn":

            temp_piece.has_moved = True


        if temp_piece.__class__.__name__ == "Pawn" and (case_temp[0] == 7 or case_temp[0] == 0):
            color_temp = "white" if tour else "black"
            temp_piece = Queen(color_temp,case_temp[0],case_temp[1],1,self.windows)
            print "ifsldjksdffsmd"

        if temp_piece.__class__.__name__ == "Pawn" and self.selected[0][1][0] == 3 and tour:
            if case_temp[1]!=self.selected[0][1][1] and not self.board[case_temp[0]][case_temp[1]]:
                self.board[3][case_temp[1]] = None
                self.draw_rectangle(3,case_temp[1])

        if temp_piece.__class__.__name__ == "Pawn" and self.selected[0][1][0] == 4 and not tour:
            if case_temp[1]!=self.selected[0][1][1] and not self.board[case_temp[0]][case_temp[1]]:
                self.board[4][case_temp[1]] = None
                self.draw_rectangle(4,case_temp[1])

        if temp_piece.__class__.__name__ == "King" and self.selected[0][1][1] == 4 and case_temp[1]!=3 and case_temp[1]!=4 and case_temp[1]!=5:
            color_temp = "white" if tour else "black"
            if case_temp[0] == 0:
                if case_temp[1] == 2:
                    self.board[0][0] = None
                    self.draw_rectangle(0,0)
                    self.board[0][3] = Rook(color_temp,0,3,1,self.windows)
                    self.board[0][3].draw_piece()
                else:
                    self.board[0][7] = None
                    self.draw_rectangle(0,7)
                    self.board[0][5] = Rook(color_temp,0,5,1,self.windows)
                    self.board[0][5].draw_piece()
            else:
                if case_temp[1] == 2:
                    self.board[7][0] = None
                    self.draw_rectangle(7,0)
                    self.board[7][3] = Rook(color_temp,7,3,1,self.windows)
                    self.board[7][3].draw_piece()
                else:
                    self.board[7][7] = None
                    self.draw_rectangle(7,7)
                    self.board[7][5] = Rook(color_temp,7,5,1,self.windows)
                    self.board[7][5].draw_piece()




        if self.board[case_temp[0]][case_temp[1]]:
            move_name += 'x'
        else:
            move_name += 'o'


        self.board[case_temp[0]][case_temp[1]] = temp_piece
        move_name += ''.join(str(e) for e in case_temp)

        if tour:
            self.moves_white.append(move_name)
        else :
            self.moves_black.append(move_name)

        self.case_unselect()
        self.draw_rectangle(case_temp[0],case_temp[1])
        temp_piece.draw_piece()
