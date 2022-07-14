import math
import random
import copy
from ordered_set import OrderedSet
import numpy as np

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
            UCB = (float(current_node.score / current_node.visits) + 2 * math.sqrt((np.log(parent_node.visits)) / current_node.visits)       
            )
        else:
            UCB = (float(current_node.loss / current_node.visits) + 15 *math.sqrt((np.log(parent_node.visits)) / current_node.visits)       # loss not score
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


global e

e = 0 
def expansion(current_node):
    
    for move in b.legalmoves():
        
        b.move(move)
        
        #b.printboard()
        
        current_node.children[move] = Nodes(0)
        
        b.undo(move)
    
    
def rollout(current_node):
    
    while (b.win() == False) and (len(b.legalmoves()) != 0):
        
        moves = b.legalmoves()
        
        move = random.choice(moves)
        
        b.move(move)
        
    result = b.win()
    
    if result == False:
        result = 0 
        
    current_node.reward = result
    
    
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
for i in range(150000):
    if i % 10000 == 0:
        print(i)
    b.resetboard()
    List = []   # for backprop
    current = selection(rootnode,List)
   # b.printboard()
    if current.terminal == False:
        if current.visits == 0:
            rollout(current)    # till terminal state reached
            backpropagate(current, List) # change number of visits and score
        
        
        else:
            e += 1
            expansion(current)
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
print('total expansions=',e)        
            



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


# computer first
'''
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

'''
#human
b.resetboard()
current = rootnode
while b.win() == False:
    b.printboard()
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

    test = ""
    for x in current.children:
        if x != -math.inf:
            test = test + "," + str(x.score/x.visits) + "|visits:" + str(x.visits) + "|"
        else:
            test = test + "," + "blank"
    move = Bestmove(current)
    print(test)
    b.move(move)
    current = current.children[move]
'''





















'''

print('TABLE')
print('ROOTNODE')
print(rootnode)

print('ONE MOVE INTO GAME')
print('----------------')


for child in rootnode.children:
    print(child.visits)            # produces 9 
    
    
print('TWO MOVES INTO GAME')
print('---------------')


count = 0

for child in rootnode.children:
    print('--------------')
    for secondarychild in child.children:
        count +=1
        try:
            print(secondarychild.visits)
        except:
            print('-inf')


print(count)


for child in rootnode.children:
    print('===================')
    for secondarychild in child.children:
        print('--------------')
        try:
            for third in secondarychild.children:
       
                try:
                    print(third.visits)
                except:
                    print('-inf')
        except:
            
            print('broke')



'''





