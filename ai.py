import random
import numpy as np

class ai :

        def __init__(self,brd,color,game):
            self.brd = brd
            self.color = color
            self.game = game
            self.depth = 4
            self.color_opponent = "black" if self.color == "white" else "white"
            self.tour = True if self.color == "white" else False
            self.final_move = None
            self.evaluate_king_white = np.array([[-3,-4,-4,-5,-5,-4,-4,-3],[-3,-4,-4,-5,-5,-4,-4,-3],[-3,-4,-4,-5,-5,-4,-4,-3],[-3,-4,-4,-5,-5,-4,-4,-3],
                                   [-2,-3,-3,-4,-4,-3,-3,-2],[-1,-2,-2,-2,-2,-2,-2,-1],[2,2,0,0,0,0,2,2],[2,3,1,0,0,1,3,2]])
            self.evaluate_queen_white = np.array([[-2,-1,-1,-0.5,-0.5,-1,-1,-2],[-1,0,0,0,0,0,0,-1],[-1,0,0.5,0.5,0.5,0.5,0,-1],[-0.5,0,0.5,0.5,0.5,0.5,0,-0.5],
                                   [0,0,0.5,0.5,0.5,0.5,0,0.5],[-1,0.5,0.5,0.5,0.5,0.5,0,-1],[-1,0,0.5,0,0,0,0,-1],[-2,-1,-1,-0.5,-0.5,-1,-1,-2]])
            self.evaluate_rook_white = np.array([[0,0,0,0,0,0,0,0],[0.5,1,1,1,1,1,1,0.5],[-0.5,0,0,0,0,0,0,-0.5],[-0.5,0,0,0,0,0,0,-0.5],[-0.5,0,0,0,0,0,0,-0.5],
                                  [-0.5,0,0,0,0,0,0,-0.5],[-0.5,0,0,0,0,0,0,-0.5],[0,0,0,0.5,0.5,0,0,0]])
            self.evaluate_knight_white = np.array([[-5,-4,-3,-3,-3,-3,-4,-5],[-4,-2,0,0,0,0,-2,-4],[-3,0,1,1.5,1.5,1,0,-3],[-3,0.5,1.5,2,2,1.5,0.5,-3],
                                [-3,0,1.5,2,2,1.5,0,-3],[-3,0.5,1,1.5,1.5,1,0.5,-3],[-4,-2,0,0.5,0.5,0,-2,-4],[-5,-4,-3,-3,-3,-3,-4,-5]])
            self.evaluate_bishop_white = np.array([[-2,-1,-1,-1,-1,-1,-1,-2],[-1,0,0,0,0,0,0,-1],[-1,0,0.5,1,1,0.5,0,-1],[-1,0.5,0.5,1,1,0.5,0.5,-1],
                                  [-1,0,1,1,1,1,0,-1],[-1,1,1,1,1,1,1,-1],[-1,0.5,0,0,0,0,0.5,-1],[-2,-1,-1,-1,-1,-1,-1,-2]])

            self.evaluate_pawn_white = np.array([[0,0,0,0,0,0,0,0],[5,5,5,5,5,5,5,5],[1,1,2,3,3,2,1,1],[0.5,0.5,1,2.5,2.5,1,0.5,0.5],[0,0,0,2,2,0,0,0],
                                  [0.5,-0.5,-1,0,0,-1,-0.5,0.5],[0.5,1,1,-2,-2,1,1,0.5],[0,0,0,0,0,0,0,0]])
            self.evaluate_king_black = np.copy(self.evaluate_king_white)
            self.evaluate_king_black[[0,1,2,3,4,5,6,7]] = self.evaluate_king_black[[7,6,5,4,3,2,1,0]]
            self.evaluate_queen_black = np.copy(self.evaluate_queen_white)
            self.evaluate_queen_black[[0,1,2,3,4,5,6,7]] = self.evaluate_queen_black[[7,6,5,4,3,2,1,0]]
            self.evaluate_rook_black = np.copy(self.evaluate_rook_white)
            self.evaluate_rook_black[[0,1,2,3,4,5,6,7]] = self.evaluate_rook_black[[7,6,5,4,3,2,1,0]]
            self.evaluate_knight_black = np.copy(self.evaluate_knight_white)
            self.evaluate_knight_black[[0,1,2,3,4,5,6,7]] = self.evaluate_knight_black[[7,6,5,4,3,2,1,0]]
            self.evaluate_bishop_black = np.copy(self.evaluate_bishop_white)
            self.evaluate_bishop_black[[0,1,2,3,4,5,6,7]] = self.evaluate_bishop_black[[7,6,5,4,3,2,1,0]]
            self.evaluate_pawn_black = np.copy(self.evaluate_pawn_white)
            self.evaluate_pawn_black[[0,1,2,3,4,5,6,7]] = self.evaluate_pawn_black[[7,6,5,4,3,2,1,0]]


        def find_move_possible(self,check,color):

            move_possible = []
            for row in range(8):
                for col in range(8):
                    piece = self.brd.board[row][col]
                    if piece and piece.color == color :
                        cases = piece.possible_cases(self.brd.board,self.brd.moves_white,self.brd.moves_black,check)
                        cases = [[piece]+x for x in cases]
                        move_possible += cases

            return move_possible

        def play_random(self,check):

            move_possible = self.find_move_possible(check,self.color)
            rng = random.randint(0,len(move_possible)-1)
            temp_piece = move_possible[rng].pop(0)

            self.brd.queek_move(temp_piece,move_possible[rng],check,self.tour)

        # def play(self,check):
        #
        #     move_possible = self.find_move_possible(check,self.color)
        #     max_evaluation = 0
        #     final_move = None
        #
        #
        #     for move in move_possible :
        #
        #         row,col = move[0].row, move[0].col
        #         row_after,col_after = move[1:]
        #         temp1 = self.brd.board[row][col]
        #         temp2 = self.brd.board[row_after][col_after]
        #         self.brd.board[row][col] = None
        #         self.brd.board[row_after][col_after] = move[0]
        #         evaluation_board = self.evaluate_board(self.color)
        #         if evaluation_board >= max_evaluation :
        #             max_evaluation = evaluation_board
        #             final_move = move
        #         self.brd.board[row][col] = temp1
        #         self.brd.board[row_after][col_after] = temp2
        #
        #     temp_piece = final_move.pop(0)
        #
        #     self.brd.queek_move(temp_piece,final_move,check,self.tour)

        def play(self,check):

            self.minimax(True,self.depth)

            temp_piece = self.final_move.pop(0)

            self.brd.queek_move(temp_piece,self.final_move,check,self.tour)

            self.final_move = None

        def minimax(self,tour,temp_depth):

            if temp_depth == 0:
                # print self.evaluate_board()
                return self.evaluate_board()


            is_check = self.game.is_check(self.brd.board,self.brd.moves_white,self.brd.moves_black)
            move_possible = self.find_move_possible(is_check,self.color) if tour else self.find_move_possible(is_check,self.color_opponent)
            tour_evaluation = -10000 if tour else 10000
            final_move = None

            for move in move_possible :

                # if temp_depth == 1:
                #     print "-------------"
                #     print self.final_move
                #     print move
                #     print "-------------"

                row,col = move[0].row, move[0].col
                row_after,col_after = move[1:]
                temp1 = self.brd.board[row][col]
                temp2 = self.brd.board[row_after][col_after]
                self.brd.board[row][col] = None
                self.brd.board[row_after][col_after] = move[0]
                evaluation_board = self.minimax(not tour,temp_depth-1)

                if tour and evaluation_board >= tour_evaluation :
                    tour_evaluation = evaluation_board
                    if temp_depth == self.depth:
                        self.final_move = move
                elif (not tour) and evaluation_board <= tour_evaluation:
                    tour_evaluation = evaluation_board

                self.brd.board[row][col] = temp1
                self.brd.board[row_after][col_after] = temp2


            return tour_evaluation




            temp_piece = final_move.pop(0)

            self.brd.queek_move(temp_piece,final_move,check,self.tour)

        def evaluate_board(self):

            value_board = 0

            for row in range(8):
                for col in range(8):
                    piece = self.brd.board[row][col]
                    if piece :

                        if piece.color == "white" :
                            if piece.__class__.__name__ == "King":
                                value = 900 + self.evaluate_king_white[row,col]
                            elif piece.__class__.__name__ == "Queen":
                                value = 90 + self.evaluate_queen_white[row,col]
                            elif piece.__class__.__name__ == "Rook":
                                value = 50 + self.evaluate_rook_white[row,col]
                            elif piece.__class__.__name__ == "Knight":
                                value = 30 + self.evaluate_knight_white[row,col]
                            elif piece.__class__.__name__ == "Bishop":
                                value = 30 + self.evaluate_bishop_white[row,col]
                            elif piece.__class__.__name__ == "Pawn":
                                value = 10 + self.evaluate_pawn_white[row,col]
                            value_board += value

                        else :
                            if piece.__class__.__name__ == "King":
                                value = 900 + self.evaluate_king_black[row,col]
                            elif piece.__class__.__name__ == "Queen":
                                value = 90 + self.evaluate_queen_black[row,col]
                            elif piece.__class__.__name__ == "Rook":
                                value = 50 + self.evaluate_rook_black[row,col]
                            elif piece.__class__.__name__ == "Knight":
                                value = 30 + self.evaluate_knight_black[row,col]
                            elif piece.__class__.__name__ == "Bishop":
                                value = 30 + self.evaluate_bishop_black[row,col]
                            elif piece.__class__.__name__ == "Pawn":
                                value = 10 + self.evaluate_pawn_black[row,col]
                            value_board -= value


            return value_board
