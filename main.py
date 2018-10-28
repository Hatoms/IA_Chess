#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import copy
from board import *
from chess_game import *
from ai import *

size_windows = 580
margin_left = 50
margin_top = 50
size_case = 60

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


def motion_ia(event):
    x, y = event.x, event.y

    if game.tour and my_ai.color == "white":
        ia_play()
    elif game.tour and my_ai.color == "black":
        manual_play(x, y)
    elif (not game.tour) and my_ai.color == "black":
        ia_play()
    else:
        manual_play(x, y)
        


def manual_play(x, y):
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
            game.ia_start = True
        else:
            game.is_selected = brd.piece_selected(x,y,game.tour,game.check)
    else:
        game.is_selected = brd.piece_selected(x,y,game.tour,game.check)

def ia_play():
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



if len(sys.argv) > 1 and sys.argv[1] == 'multi':
    func = locals()["motion"]
else:
    func = locals()["motion_ia"]

root = Tk()
root.title('chess')
brd = Board(size_windows, margin_left, margin_top, size_case, root)
game = ChessGame()
my_ai = ai(brd,"white",game)

root.bind('<Button-1>', func)

root.mainloop()