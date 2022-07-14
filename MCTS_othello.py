import math
import random
import copy
from ordered_set import OrderedSet
import numpy as np


class Board:
    def __init__(self):
        self.player = 1
        self.board = np.zeros((8, 8), dtype=int)
        self.board[3, 3] = 1
        self.board[3, 4] = 2
        self.board[4, 4] = 1
        self.board[4, 3] = 2
        
       # self.cantmove = 0

    def resetboard(self):
        self.board = np.zeros((8, 8), dtype=int)
        self.board[3, 3] = 1
        self.board[3, 4] = 2
        self.board[4, 4] = 1
        self.board[4, 3] = 2
        self.player = 1
        
        #self.cantmove = 0 # added

    def legalmoves(self):
        availablemoves = []
        if self.player == 1:
            otherplayer = 2
        else:
            otherplayer = 1

        for move in np.argwhere(self.board == otherplayer): 
            xlist = [-1, 0, 1, 1, 1, 0, -1, -1]
            ylist = [-1, -1, -1, 0, 1, 1, 1, 0]
            for direction in range(0, 8):
                xadj = xlist[direction]
                yadj = ylist[direction]
                tile = copy.deepcopy(move)

                tile[0] = tile[0] + xadj
                tile[1] = tile[1] + yadj

                playablespace = copy.deepcopy(tile)
                if (playablespace[0] in range(0,8)) and (playablespace[1] in range(0,8)):
                    
                    try:
                        if self.board[tile[0], tile[1]] == 0:
                            backtrack = True
                            
                            xrev = xadj * -1
                            yrev = yadj * -1
    
                            tile[0] = tile[0] + xrev
                            tile[1] = tile[1] + yrev
                       
                            while backtrack == True:
                                try:
                                    if (self.board[tile[0], tile[1]] == self.player) or (self.board[tile[0], tile[1]] == 0) :
                                        backtrack = False
                                    TESTcopy = copy.deepcopy(tile)
        
                                    xrev = xadj * -1
                                    yrev = yadj * -1
        
                                    tile[0] = tile[0] + xrev
                                    tile[1] = tile[1] + yrev
                                    if tile[0] < 0:
                                        tile[0] = 100
                                    if tile[1] < 0:
                                        tile[1] = 100
                                    if tile[0] > 7:
                                        tile[0] = 100
                                    if tile[1] > 7:
                                        tile[1] = 100
        
                                except:
                                    backtrack = False
        
                            if (backtrack == False) and (
                                self.board[TESTcopy[0], TESTcopy[1]] == self.player
                            ):
                                playablespace = playablespace.tolist()
                                if playablespace not in availablemoves:
                                    availablemoves.append(playablespace)
                    except:
                        pass

        return availablemoves

    def win(self):
        zero = 0
        X = 0
        O = 0
        for row in self.board:
            for space in row:
                if space == 0:
                    zero += 1
                if space == 1:
                    X += 1
                if space == 2:
                    O += 1
        '''
        if (zero == 0):
            #print('Game end')
            if X > O:
                return 1
            if O > X:
                return -1
            if X == O:
                return int(0)    # changed to int
        '''
        
        if (len(self.legalmoves()) == 0): # if current player has no legalmoves
            b.change_player()              # change player
            if (len(self.legalmoves()) == 0): # check if other player has any moves
                #print('Game end')
                if X > O:
                    return 1
                if O > X:
                    return -1
                if X == O:
                    return 2 
            else:
                b.change_player() # change player back
                return False
        else:
            return False
            

    def move(self, position):

        if self.player == 1:
            otherplayer = 2
        else:
            otherplayer = 1
       # print('------')
        #print('player from move section:',self.player)

       # print('-----')
        if position in self.legalmoves():
            xlist = [-1, 0, 1, 1, 1, 0, -1, -1]
            ylist = [-1, -1, -1, 0, 1, 1, 1, 0]
            global changelist
            changelist = []
            coords = [0,1,2,3,4,5,6,7]
            for direction in range(0, 8):
                xadj = xlist[direction]
                yadj = ylist[direction]
                tile = copy.deepcopy(position)
                
                
                tile[0] = tile[0] + xadj
                tile[1] = tile[1] + yadj
                tile_list = []
                END = False
                while (tile[0] in coords) and (tile[1] in coords) and (END == False) and (self.board[tile[0], tile[1]] != 0):
                    tile2 = copy.deepcopy(tile)
                    if (self.board[tile[0], tile[1]] == otherplayer):
                        tile_list.append(tile2)
                    
                    if tile2[0] < 0:
                        tile2[0] = 100
                        END =True
                    if tile2[1] < 0:
                        tile2[1] = 100
                        END = True

                    try:

                        if self.board[tile[0], tile[1]] == self.player:
                            for space in tile_list:
                                space2 = copy.deepcopy(space)
                                changelist.append(space2)
                                END = True
                            
                    
                    except:
                        pass
                    tile[0] = tile[0] + xadj
                    tile[1] = tile[1] + yadj

            if self.player == 1:
                self.board[position[0], position[1]] = 1
                for t in changelist:

                    self.board[t[0],t[1]] = 1
            else:
                self.board[position[0], position[1]] = 2
                for t in changelist:
                    self.board[t[0],t[1]] = 2
        else:
            print("Invalid move, space allready used")
            print('Attempted move=',position)
            print('you are player:',self.player)
            print(self.legalmoves())
            position = str(input("Enter coordinates: "))
    
            position = [int(position[0]),int(position[1])]
            self.move(position)
            return
        
        if self.player == 1:
            self.player = 2
            

        else:
            self.player = 1
            
            
    def undo(self, position):
        self.board[position[0], position[1]] = 0
        if self.player == 1:
            self.player = 2
            for t in changelist:
                self.board[t[0],t[1]] = 1
        else:
            self.player = 1
            for t in changelist:
                self.board[t[0],t[1]] = 2

    def printboard(self):
        
        print(self.board)
        '''
        print('\n')
        for row in self.board:
            print(
                str(row[0])
                + "|"
                + str(row[1])
                + "|"
                + str(row[2])
                + "|"
                + str(row[3])
                + "|"
                + str(row[4])
                + "|"
                + str(row[5])
                + "|"
                + str(row[6])
                + "|"
                + str(row[7])
            )
            print("----------------")
            '''
        
        
        
        
        
    
        
    def gamestate(self):
        return (self.board,self.player)

    def spacenumber(self, move):
        a = np.array(
            [
                [0, 1, 2, 3, 4, 5, 6, 7],
                [8, 9, 10, 11, 12, 13, 14, 15],
                [16, 17, 18, 19, 20, 21, 22, 23],
                [24, 25, 26, 27, 28, 29, 30, 31],
                [32, 33, 34, 35, 36, 37, 38, 39,],
                [40, 41, 42, 43, 44, 45, 46, 47],
                [48, 49, 50, 51, 52, 53, 54, 55],
                [56, 57, 58, 59, 60, 61, 62, 63],
            ]
        )
        
        
        if type(move) == int:
            new_move = list(np.argwhere(a == move))     
            new_move = list(new_move[0])

        else:
            
            new_move = int(a[move[0], move[1]])        # changed to int
        return new_move
    
    
    def changegameboard(self,newboard,newplayer):
        self.board = newboard
        
        self.player = newplayer
        
    
    
    def reset_cantmove(self):
        
        self.cantmove = 0
        
        
        
        
       
    def change_player(self):
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1
    
    
    def Turn(self):

        return (self.player)
    
    
    
    

b = Board()


class Nodes:
    def __init__(self,result):
        self.visits = 0
        self.score = 0
        self.loss = 0
        if (b.win() != False) or ((len(b.legalmoves())) == 0):  

            self.terminal = True  

        else:
            self.terminal = False

        self.children = [-math.inf for _ in range(64)] # set to 64 for the number of squares

        self.reward = result
        

def ucb1(current_node, parent_node,turn):

    if current_node.visits == 0:
        return math.inf
    else:
        if turn == 1:
            UCB = ( float(current_node.score / current_node.visits) + 200 *math.sqrt((np.log(parent_node.visits)) / current_node.visits)       
            )
        else:
            UCB = (float(current_node.loss / current_node.visits) - 200 *math.sqrt((np.log(parent_node.visits)) / current_node.visits)       # loss not score
            )
    return UCB
    

def selection(current_node,List):
    
    List.append(current_node)
    
    first = True
    Leaf = False
    
    
    if current_node.children == [-math.inf for _ in range(64)]: # also changed to 64
        Leaf = True
    
    if (current_node.terminal == True) or (Leaf == True):
        return(current_node) 
    
    
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
                if UCB1 == math.inf:
                    UCB1 = -math.inf
                
                if first == True:
                    Max_value = UCB1
                    bestchild = child
                    bestmove = current_node.children.index(child)
                    first = False
                
                if UCB1 < Max_value:   # changed this to less than to minimise??
                    Max_value = UCB1
                    bestchild = child
                    bestmove = current_node.children.index(child)
                    
                    
    bestmove = b.spacenumber(bestmove)  
        
    b.move(bestmove)
    
    return(selection(bestchild,List))
    
    
def expansion(current_node):
    for move in b.legalmoves():
        
        b.move(move)
        move = b.spacenumber(move)           # change from coords to numbers
        current_node.children[move] = Nodes(0)
        move = b.spacenumber(move)            # change from coords to numbers
        b.undo(move)
    
    
def rollout(current_node):
    
    while (b.win() == False) :       # removed --> and (len(b.legalmoves()) != 0)
        try:
            moves = b.legalmoves()
            
            move = random.choice(moves)
            #print(move)
            b.move(move)
            
        except:
            #print('change player')
            b.change_player()
            pass
    result = b.win()
    if result == 2 or result == False:
        result = 0 
        
    current_node.reward = result
    
    
def backpropagate(current,List):
    
    outcome = current.reward
    
    for node in List:
        if outcome == -1:
            node.loss += 1
        if outcome == 1:
            node.score += 1
        if outcome == 0:
            node.score += 0
            node.loss += 0
          
        node.visits += 1
    
    
    
    
b.resetboard()
rootnode = Nodes(0)

for i in range(100):
    if i % 10000 == 0:
        print(i)
    b.resetboard()
    List = []   # for backprop
    current = selection(rootnode,List)
    
    if current.terminal == False:
        if current.visits == 0:
            rollout(current)    # till terminal state reached
            backpropagate(current, List) # change number of visits and score
        
        
        else:

            expansion(current)
            for child in range(0,64):
                if current.children[child] != -math.inf:
                    current = current.children[child]
                    break# the first child node
            
            List.append(current)
            rollout(current)
            backpropagate(current,List)
        

    else: # game is terminal state, maybe doesnt work??
        #b.printboard()
    
        rollout(current)
        backpropagate(current,List)
            
       
            
       
        
       
        
       
        
def MCTS(current_node):
    ###run mcts a number of times before each move###
    
    boardcopy,playercopy = copy.deepcopy(b.gamestate())
    boardtest = copy.deepcopy(boardcopy)
    
    
    print('player begining of MCTS:',playercopy)
    
    for i in range(1000):
        if i % 10 == 0:
            
            print(i)
        boardtest = copy.deepcopy(boardcopy)
        
        b.changegameboard(boardtest,playercopy) #issue!!!!!!!!!!!!!!!!

        bo,p = b.gamestate()
        
       # print('player=',p)
       # b.printboard()
        List = []   
        current = selection(current_node,List) 
        
        if current.terminal == False:
            if current.visits == 0:
                rollout(current)   
                backpropagate(current, List) 
            
            
            else:
    
                expansion(current)
                for child in range(0,64):
                    if current.children[child] != -math.inf:
                        current = current.children[child]
                        break
                
                List.append(current)
                rollout(current)
                backpropagate(current,List)
            
        else: 
            
            rollout(current)
            backpropagate(current,List)
    

    b.changegameboard(boardcopy,playercopy)
    b.reset_cantmove()

def Bestmove(current_node):
    
    
    ### bestmove function###
    
    max_value = -100000
    bestmove = -1
    if current_node != -math.inf:
        for child in range(0, len(current_node.children)):
            if child in b.legalmoves():

                if current_node.children[child] != -math.inf:
                    value = current_node.children[child].score

                    if value > max_value:
                        max_value = value
                        #bestchild = current_node.children[child]
                        bestmove = child

    if bestmove == -1:
        moves = b.legalmoves()
        try:
            bestmove = random.choice(moves)
        except:
            pass
    
    
    
    
    return bestmove


b.resetboard()
gamestate = rootnode
while b.win() == False:
    print(b.legalmoves())
    MCTS(gamestate)
    move = Bestmove(gamestate)
    
    if move == -1:
        b.change_player()
    else:
        b.move(move)
        
        b.printboard()
        
        test = ""
        #print(gamestate)
        for x in gamestate.children:
            if x != -math.inf:
                test = test + "," + str(x.score) + "|visits:" + str(x.visits) + "|"
            else:
                test = test + "," + "blank"
        
        move = b.spacenumber(move)
        try:
            gamestate = gamestate.children[move]
        except:
            pass
        
    print(test)

    print(b.legalmoves())
    if len(b.legalmoves()) == 0:
        b.change_player()
    else:
        move = str(input("Enter coordinates Y then X: "))
        move = [int(move[0]),int(move[1])]
        b.move(move)
        b.printboard()
        test = ""
        for x in gamestate.children:
            if x != -math.inf:
                test = test + "," + str(x.score) + "|visits:" + str(x.visits) + "|"
            else:
                test = test + "," + "blank"
        
        move = b.spacenumber(move)
        try:
            gamestate = gamestate.children[move]
        except:
            pass
        #print(gamestate)
        print(test)

