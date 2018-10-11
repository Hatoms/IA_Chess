#!/usr/bin/env python
#-*- coding: utf-8 -*-


import copy
from board import *
from chess_game import *
from ai import *

size_windows = 580
margin_left = 50
margin_top = 50
size_case = 60
root = Tk()
root.title('chess')

brd = Board(size_windows, margin_left, margin_top, size_case, root)
game = ChessGame()

def motion(event):

    x, y = event.x, event.y


    if game.is_selected:
        if brd.try_moving(x,y,game.check,game.tour):
            game.is_selected = False
            game.is_check(brd.board,brd.moves_white,brd.moves_black)

            if game.check :
                brd.draw_check(game.tour)
            if game.is_checkmate(brd.board,brd.moves_white,brd.moves_black):
                winner = "Whites" if game.tour else "Black"
                button_end = Button(brd.root, text = '%s win by checkmate ! Try again ?'%winner, command = exit)
                button_end.pack()

            if game.is_draw(brd.board,brd.moves_white,brd.moves_black):
                button_draw = Button(brd.root, text = 'Draw : %s'%game.draw_message, command = exit)
                button_draw.pack()
            game.tour = not game.tour

        else:
            game.is_selected = brd.piece_selected(x,y,game.tour,game.check)
    else:
        game.is_selected = brd.piece_selected(x,y,game.tour,game.check)



my_ai = ai(brd,"white",game)
def motion_ia(event):

    x, y = event.x, event.y

    if game.tour :
        my_ai.play(game.check)

        game.is_selected = False
        game.is_check(brd.board,brd.moves_white,brd.moves_black)

        if game.check :
            brd.draw_check(game.tour)
        if game.is_checkmate(brd.board,brd.moves_white,brd.moves_black):
            winner = "Whites" if game.tour else "Black"
            button_end = Button(brd.root, text = '%s win by checkmate ! Try again ?'%winner, command = exit)
            button_end.pack()

        if game.is_draw(brd.board,brd.moves_white,brd.moves_black):
            button_draw = Button(brd.root, text = 'Draw : %s'%game.draw_message, command = exit)
            button_draw.pack()
        game.tour = not game.tour

    else:
        if game.is_selected:
            if brd.try_moving(x,y,game.check,game.tour):
                game.is_selected = False
                game.is_check(brd.board,brd.moves_white,brd.moves_black)

                if game.check :
                    brd.draw_check(game.tour)
                if game.is_checkmate(brd.board,brd.moves_white,brd.moves_black):
                    winner = "Whites" if game.tour else "Black"
                    button_end = Button(brd.root, text = '%s win by checkmate ! Try again ?'%winner, command = exit)
                    button_end.pack()

                if game.is_draw(brd.board,brd.moves_white,brd.moves_black):
                    button_draw = Button(brd.root, text = 'Draw : %s'%game.draw_message, command = exit)
                    button_draw.pack()
                game.tour = not game.tour

            else:
                game.is_selected = brd.piece_selected(x,y,game.tour,game.check)
        else:
            game.is_selected = brd.piece_selected(x,y,game.tour,game.check)



root.bind('<Button-1>', motion_ia)

root.mainloop()
