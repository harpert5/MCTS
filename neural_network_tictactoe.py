
import math
import random
import copy
from ordered_set import OrderedSet
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt
from numpy import asarray
from numpy import argmax
from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
import os
import tensorflow as tf
import time
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.get_logger().setLevel('ERROR')
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

class Board:
    def __init__(self):
        self.player = 1
        self.board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]

    def resetboard(self):
        self.board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
        self.player = 1

    def legalmoves(self):
        availablemoves = []
        for move in range(0, 9):
            if self.board[move] == " ":
                availablemoves.append(move)
        return availablemoves

    def win(self):
        if (
            self.board[0] == self.board[1]
            and self.board[0] == self.board[2]
            and self.board[0] != " "
        ):
            if self.board[0] == "O":
                return -1
            else:
                return 1
        elif (
            self.board[3] == self.board[4]
            and self.board[3] == self.board[5]
            and self.board[3] != " "
        ):
            if self.board[3] == "O":
                return -1
            else:
                return 1
        elif (
            self.board[6] == self.board[7]
            and self.board[6] == self.board[8]
            and self.board[6] != " "
        ):
            if self.board[6] == "O":
                return -1
            else:
                return 1
        elif (
            self.board[0] == self.board[3]
            and self.board[0] == self.board[6]
            and self.board[0] != " "
        ):
            if self.board[0] == "O":
                return -1
            else:
                return 1
        elif (
            self.board[1] == self.board[4]
            and self.board[1] == self.board[7]
            and self.board[1] != " "
        ):
            if self.board[1] == "O":
                return -1
            else:
                return 1
        elif (
            self.board[2] == self.board[5]
            and self.board[2] == self.board[8]
            and self.board[2] != " "
        ):
            if self.board[2] == "O":
                return -1
            else:
                return 1
        elif (
            self.board[0] == self.board[4]
            and self.board[0] == self.board[8]
            and self.board[0] != " "
        ):
            if self.board[0] == "O":
                return -1
            else:
                return 1
        elif (
            self.board[6] == self.board[4]
            and self.board[6] == self.board[2]
            and self.board[6] != " "
        ):
            if self.board[6] == "O":
                return -1
            else:
                return 1
        else:
            return False

    def move(self, position):

        if position in self.legalmoves():
            if self.player == 1:
                self.board[position] = "X"
            else:
                self.board[position] = "O"

        else:
            print("Invalid move, space allready used")
            position = int(input("Enter position: "))
            self.move(position)
            return

        if self.player == 1:
            self.player = 2

        else:
            self.player = 1

    def undo(self, position):

        self.board[position] = " "
        if self.player == 1:
            self.player = 2

        else:
            self.player = 1

    def printboard(self):
        print(self.board[0] + "|" + self.board[1] + "|" + self.board[2])
        print("-+-+-")
        print(self.board[3] + "|" + self.board[4] + "|" + self.board[5])
        print("-+-+-")
        print(self.board[6] + "|" + self.board[7] + "|" + self.board[8])

    def gamestate(self):
        return self.board
    
    def Turn(self):

        return (self.player)


b = Board()


class Nodes:
    def __init__(self,result):
        self.visits = 0
        self.score = 0
        self.loss = 0
        if (b.win() != False) or ((len(b.legalmoves())) == 0):  # added the draw section

            self.terminal = True  # can change from if

        else:
            self.terminal = False

        self.children = [-math.inf for _ in range(9)]

        self.reward = result
        

def ucb1(current_node, parent_node,turn):

    if current_node.visits == 0:
        return math.inf
    else:
        if turn == 1:
            UCB = (float(current_node.score / current_node.visits) + 5 * math.sqrt((np.log(parent_node.visits)) / current_node.visits)       
            )
        else:
            UCB = (float(current_node.loss / current_node.visits) + 10 *math.sqrt((np.log(parent_node.visits)) / current_node.visits)       # loss not score
            )
        return UCB

 # float(current_node.loss / current_node.visits) + 15 *
# float(current_node.score / current_node.visits) + 2 *

def selection(current_node,List):
    
    List.append(current_node) # create list for backprop
    
    first = True
    Leaf = False
    
    
    if current_node.children == [-math.inf for _ in range(9)]:
        Leaf = True
    
    
    if (current_node.terminal == True) or (Leaf == True):
        

        return(current_node) 
    
    
    # loop section
    if b.Turn() == 1:
        for child in current_node.children:
            if child != -math.inf:
    
                UCB1 = ucb1(child,current_node,1) 
                #print(UCB1)
                if first == True:
                    Max_value = UCB1
                    bestchild = child
                    bestmove = current_node.children.index(child)
                    first = False
                
                if UCB1 > Max_value:
                    Max_value = UCB1
                    bestchild = child
                    bestmove = current_node.children.index(child) 
    else:
        for child in current_node.children:
            if child != -math.inf:
    
                UCB1 = ucb1(child,current_node,2) 
               # print(UCB1)
               # if UCB1 == math.inf:
                 #   UCB1 = -math.inf
                
                if first == True:
                    Max_value = UCB1
                    bestchild = child
                    bestmove = current_node.children.index(child)
                    first = False
                
                if UCB1 > Max_value:   # changed this to less than to minimise??
                    Max_value = UCB1
                    bestchild = child
                    bestmove = current_node.children.index(child) 
    


    b.move(bestmove)
    
    return(selection(bestchild,List))







def neural_network(X_train,y_train):
    
    X_train = asarray([X_train])
    y_train = asarray([y_train])

    
    try:
        model = load_model('model.h1')
    
    except OSError:
        n_inputs = 9
        n_outputs = 9
        model = Sequential()
        model.add(Dense(20, activation='relu', kernel_initializer='he_uniform',input_dim = n_inputs ))
        #model.add(Dense(8, activation='relu', kernel_initializer='he_normal'))
        model.add(Dense(n_outputs, kernel_initializer='he_uniform'))
        model.compile(optimizer='adam', loss='mae')

    model.fit(X_train, y_train)
    model.save('model.h1')
    


def predict(board):
    
    try:
        model = load_model('model.h1')
    
    except OSError:
        n_inputs = 9
        n_outputs = 9
        model = Sequential()
        model.add(Dense(20, activation='relu', kernel_initializer='he_uniform',input_dim = n_inputs ))
        #model.add(Dense(8, activation='relu', kernel_initializer='he_normal'))
        model.add(Dense(n_outputs, kernel_initializer='he_uniform'))
        model.compile(optimizer='adam', loss='mae')
        model.save('model.h1')
    board2 = asarray([board])
    prediction = model(board2)

    return prediction





    
def rollout(current_node):
    trainboard = b.gamestate()
    X_train = []
    for space in trainboard:
            if space == ' ':
                X_train.append(0)
            elif space == 'X':
                X_train.append(1)
            elif space == 'O':
                X_train.append(2)

    while (b.win() == False) and (len(b.legalmoves()) != 0):
        gameboard = b.gamestate()
        input_board = []
        for space in gameboard:
            if space == ' ':
                input_board.append(0)
            elif space == 'X':
                input_board.append(1)
            elif space == 'O':
                input_board.append(2)
        tic = time.perf_counter()
        moves = predict(input_board) 
        toc = time.perf_counter()
        print(f"prediction {toc-tic:0.4f} seconds")
        moves = moves[0]
        legal = b.legalmoves()
        bestscore = -100
        bestmove = 10
        position = 0
        if b.Turn() == 1:
            for move in moves:
                if position in legal:
                    if move > bestscore:
                        bestscore = move
                        bestmove = position
                position +=1
        else:
            bestscore = 100
            for move in moves:
                if position in legal:
                    if move < bestscore:
                        bestscore = move
                        bestmove = position
                position +=1
        b.move(bestmove)
        
        
    
    result = b.win()
    
    if result == False:
        result = 0 
        
    tic = time.perf_counter()
    neural_network(X_train,result)    
    toc = time.perf_counter()
    print(f"neural network {toc-tic:0.4f} seconds")
    current_node.reward = result
    
    
    
    
    
    
    
def expansion(current_node):
    
    for move in b.legalmoves():
        
        b.move(move)
        

        
        current_node.children[move] = Nodes(0)
        
        b.undo(move)
    
def backpropagate(current,List):
    
    outcome = current.reward


    for node in List:
        if outcome == -1:
            node.loss += 1
            # added new
            try:
                if node == List[-2]:
                    node.score = 0
            except:
                pass
        if outcome == 1:
            node.score += 1
            try:
                if node == List[-2]:
                    node.loss = 0
            except:
                pass
            
        if outcome == 0:
            node.score += 0
            node.loss += 1
          
        node.visits += 1

    


   
b.resetboard()
rootnode = Nodes(0)
count = 0
for i in range(2):
    if i % 1 == 0:
        print(i)
    b.resetboard()
    List = []   # for backprop
    tic = time.perf_counter()
    current = selection(rootnode,List)
    toc = time.perf_counter()
    print(f"selection {toc-tic:0.4f} seconds")
   # b.printboard()
    if current.terminal == False:
        if current.visits == 0:
            tic = time.perf_counter()
            rollout(current)    # till terminal state reached
            toc = time.perf_counter()
            print(f"rollout {toc-tic:0.4f} seconds")
            tic = time.perf_counter()
            backpropagate(current, List) # change number of visits and score
            toc = time.perf_counter()
            print(f"backpropagate {toc-tic:0.4f} seconds")
        
        
        else:
            tic = time.perf_counter()
            expansion(current)
            toc = time.perf_counter()
            print(f"expansion {toc-tic:0.4f} seconds")
            for child in range(0,9):
                if current.children[child] != -math.inf:
                    current = current.children[child]
                    break# the first child node
            
            List.append(current)
            rollout(current)
            backpropagate(current,List)
        

    else: # game is terminal state, maybe doesnt work??
        #b.printboard()
        count += 1
        rollout(current)
        backpropagate(current,List)
       #     
            
print('terminal state selected:',count)            

            

'''

def Bestmove(current_node):
    #bestchild = 0
    max_value = -10000000
    bestmove = -1
    if current_node != -math.inf:
        for child in range(0, len(current_node.children)):
            if child in b.legalmoves():

                if current_node.children[child] != -math.inf:
                    value = (current_node.children[child].score)/(current_node.children[child].visits)
                    #(current_node.children[child].score)/(current_node.children[child].visits)

                    if value > max_value:
                        max_value = value
                        #bestchild = current_node.children[child]
                        bestmove = child

    if bestmove == -1:
        moves = b.legalmoves()
        bestmove = random.choice(moves)

    return bestmove


b.resetboard()
current = rootnode
while b.win() == False:
    test = ""
    for x in current.children:
        if x != -math.inf:
            test = test + "," + str(x.score/x.visits) + "|visits:" + str(x.visits) + "|"
        else:
            test = test + "," + "blank"
    move = Bestmove(current)
    print(test)
    b.move(move)
    
    b.printboard()
    current = current.children[move]
    
    text = ''
    for child in current.children:
        
        if child != -math.inf:
            try:
                text = text + ','+ str(child.loss/child.visits) + "|visits:" + str(child.visits) + "|"
            except:
                text = text +',' +'No visits'
        else:
            text = text +',' +'blank'
    
    print(text)
    position = int(input("Enter position for 'O': "))
    b.move(position)
   
    b.printboard()
    current = current.children[position]
    
    '''
