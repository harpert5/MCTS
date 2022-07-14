from MCTS_tictactoe import Board

import pytest


       
def test_win():
    b = Board
    b.board = ["X", "X", "X", " ", " ", " ", " ", " ", " "]
    
    assert b.win(b) == 1
    
    b.board = ["X", " ", " ", " ", "X", " ", " ", " ", "X"]
    
    assert b.win(b) == 1
    
    b.board = [" ", " ", "X", " ", "X", " ", "X", " ", " "]
    
    assert b.win(b) == 1
    
    b.board = [" ", " ", " ", "X", "X", "X", " ", " ", " "]
    
    assert b.win(b) == 1
    
    b.board = ["O", "X", "O ", "X", "O", "X", "X", "O", "X"]
    
    assert b.win(b) == False
    
    b.board = ["O", "O", "O", " ", " ", " ", " ", " ", " "]
    
    assert b.win(b) == -1
    
    
    
    
import MCTS_tictactoe as MCTS    

def test_selection():
    
    List = []
    
    
    current_node =
    
    
    
    
    
    
    



























