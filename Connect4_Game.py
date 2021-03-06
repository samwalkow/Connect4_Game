import numpy as np
import operator
import time
from collections import deque

from numpy.lib.function_base import percentile

#defining connect 4 player1
class C4_Player:
    #initialise required variables
    def __init__(self, board, element):
        self.board = board
        self.element = element

    #call this method to make a move by asking user a user to enter their choice
    def play_your_move(self):
        print ("player ", self.element, "taking a move")
        move = int(input("enter your number: "))
        # if the column is already full, ask user to enter the correct choice
        self.board, placement = add_element(self.board,move,self.element)
        while not placement:
            print("please enter correct choice!!!")
            move = int(input("enter your number: "))
            self.board, placement = add_element(self.board,move,self.element)
        print (board)
        return self.board, move

#defining connect 4 computer bot
class C4_Bot:
    #initialise required variables
    def __init__(self, board, element, search_depth, alpha_beta):
        self.board = board
        self.element = element
        self.max_depth = search_depth
        self.alpha_beta = alpha_beta
        

    #call this method to make a move which will calculate heuristic and decides the move
    def play_your_move(self):
        global node_explored
        global node_print
        global player_human
        node_explored = 0
        time_measure = 0
        time_measure = time.time()
        if self.alpha_beta:
            alpha = -100000
            beta = 100000
            move = minimax_apha_beta_pruning(self.board, self.element, alpha, beta, True, self.max_depth, 0, game_verison)
        else:
            move = minimax(self.board, self.element, True, self.max_depth, 0)
        self.board, placement = add_element(self.board, move, self.element)
        time_measure = time.time() - time_measure
        print ("\nplayer ", self.element, "taking a move at ", move)
        print()
        print ("time taken by computer bot is: {}".format(time_measure))
        print()
        print ("number of nodes explored by computer bot is: {}".format(node_explored))
        print()
        level1 = []
        level2 = []
        level3 = []
        level4 = []
        level5 = []
        # for nodes in tree:
        #     print(nodes)
        show_nodes = input("Show the game tree? y/n: ")
        if show_nodes == 'y':
            winning_boards = []
            bot_node_wins = 0
            human_node_wins = 0
            draw_node_wins = 0
            for node in node_print:
                if node[1] == 5:
                    level5.append(node)
                if node[1] == 4:
                    level4.append(node)
                if node[1] == 3:
                    level3.append(node)
                if node[1] == 2:
                    level2.append(node)
                if node[1] == 1:
                    level1.append(node)
                if not check_game_status(node[0]):                               
                    if check_win(node[0], self.element, game_verison):
                        print("node explored by computer bot:\n", node[0])
                        print("depth level:", node[1])
                        print("Outome: Winning Node - bot wins!")
                        winning_boards.append(node)
                        bot_node_wins += 1
                    if check_win(node[0], player_human.element, game_verison):
                        print("node explored by computer bot:\n", node[0])
                        print("depth level:", node[1])
                        print("Outcome: Losing Node - human wins")
                        human_node_wins += 1
                    if not check_win(node[0], self.element, game_verison) and not check_win(node[0], player_human.element, game_verison):
                        print("node explored by computer bot:\n", node[0])
                        print("depth level:", node[1])
                        print("Outcome: Unknown - game in progress")
                    print()
                if check_game_status(node[0]) and not check_win(node[0], self.element, game_verison) and not check_win(node[0], player_human, game_verison):
                    print("node explored by computer bot:\n", node[0])
                    print("depth level:", node[1])
                    print("Outcome: a draw - no one wins")
                    draw_node_wins += 1
                    print()
            # print("Bot wins: ", bot_node_wins)
            # print("Human wins: ", human_node_wins)
            # print("Number of draws:", draw_node_wins)
            # print("Root: ", level1)
            # print("Second Level: ", level2)
            # print("Third Level: ", level3)
            # print("Fourth level: ", level4)
            # print("Final Nodes: ", level5)
            for n in winning_boards:
                
                for nn in node_print:
                    
                    if n[1] == nn[1]-1:
                        print("parent: ", n, "child ", nn)
                    else:
                        print("no parent")

    
        print()
        print("Game board:\n", self.board)
        print()
        return self.board, move


#get board and game specification from user
def get_user_input():
    width = int(input("enter board width from 1 to 10:\n"))
    height = int(input("enter board height from 1 to 10:\n"))
    game_version = int(input("enter what level of game: \n"))
    choice=input("for minimax enter: 0 and for AlphaBeta pruning enter: 1\n")
    search_level = input("enter the level of depth (<10): ")
    return width, height, choice, search_level, game_version

#creat a board of specific width and height. empty cells are marked with dot '.'
def create_board(width, height):
    #creating board
    grids = np.chararray((height,width))
    grids[:] ='.'
    #creating base of board and merge it
    base = np.chararray((1,width))
    for i in range(width):
        base[0,i] = i
    grids = np.vstack((grids,base))
    return grids


def create_key(node: list):
    board_str = ""
    for rows in node:
        for items in rows:
            board_str += str(items)
    return board_str

#add the user's or bot's element in bod as per their request
def add_element(board, position, element):
    placement = False
    height = board.shape[0]-1
    for i in range(height+1):
        if board[height-i,position]== b'.':
            board[height-i,position]=element
            current_pos = (height-i,position)
            placement = True
            break
    # print(board)
    # print()
    return board,placement

# make the very first move during start of the game for computer
def initial_move(board):
    global node_print
    root = {}
    height = board.shape[0]-1
    width = int(board.shape[1]/2)
    board[height-1][width] = 'x'
    root["root"] = board
    return board,(height-1,width)

#check if given player won the game or not
def check_win(board,player,game_version):
    tile = player
    if tile == 'o':
        tile = b'o'
    if tile == 'x':
        tile = b'x'
    rows,cols = np.shape(board)

    if game_version >= 4:
        rows = rows-1
        result = False
        #check if vertical, horizontal or diagonal four elements are same. If same declare a win
        for row in range(rows):
            for col in range(cols):
                #check horizontal entries
                try:
                    if (board[row][col] == tile and board[row][col+1] == tile and board[row][col+2] == tile and board[row][col+3] == tile):
                        result = True
                except IndexError:
                        pass
                #check vertical entries
                try:
                    if (board[row][col] == tile and board[row+1][col] == tile and board[row+2][col] == tile and board[row+3][col] == tile):
                        result = True
                except IndexError:
                        pass
                #check positive diagonal
                try:
                    if (board[row][col] == tile and board[row+1][col+1] == tile and board[row+2][col+2] == tile and board[row+3][col+3]== tile):
                        result = True
                except IndexError:
                    pass
                #check negative diagonal
                try:
                    if col-1<0 or col-2<0 or col-3<0:
                        raise IndexError
                    elif (board[row][col] == tile and board[row+1][col-1] == tile and board[row+2][col-2] == tile and board[row+3][col-3]== tile):
                        result = True
                except IndexError:
                    pass
        return result

    if game_verison ==3:
        rows = rows-1
        result = False
        #check if vertical, horizontal or diagonal four elements are same. If same declare a win
        for row in range(rows):
            for col in range(cols):
                #check horizontal entries
                try:
                    if (board[row][col] == tile and board[row][col+1] == tile and board[row][col+2] == tile):
                        result = True
                except IndexError:
                    pass
                #check vertical entries
                try:
                    if (board[row][col] == tile and board[row+1][col] == tile and board[row+2][col] == tile):
                        result = True
                except IndexError:
                    pass
                #check positive diagonal
                try:
                    if (board[row][col] == tile and board[row+1][col+1] == tile and board[row+2][col+2] == tile):
                        result = True
                except IndexError:
                    pass
                #check negative diagonal
                try:
                    if col-1 < 0 or col-2 < 0 or col-3 < 0:
                        raise IndexError
                    elif (board[row][col] == tile and board[row+1][col-1] == tile and board[row+2][col-2] == tile):
                        result = True
                except IndexError:
                    pass

        return result

    if game_version == 2:
        rows = rows-1
        result = False
        #check if vertical, horizontal or diagonal four elements are same. If same declare a win
        for row in range(rows):
            for col in range(cols):
                #check horizontal entries
                try:
                    if (board[row][col] == tile and board[row][col+1] == tile):
                        result = True
                except IndexError:
                    pass
                #check vertical entries
                try:
                    if (board[row][col] == tile and board[row+1][col] == tile):
                        result = True
                except IndexError:
                    pass
                #check positive diagonal
                try:
                    if (board[row][col] == tile and board[row+1][col+1] == tile):
                        result = True
                except IndexError:
                    pass
                #check negative diagonal
                try:
                    if col-1 < 0 or col-2 < 0 or col-3 < 0:
                        raise IndexError
                    elif (board[row][col] == tile and board[row+1][col-1] == tile):
                        result = True
                except IndexError:
                    pass

        return result

#check if game is complete or not
def check_game_status(board):
    if b'.' in board:
        return False
    else:
        return True

#calculate the utility value of each player at each move
def eval_function(board, game_verison):
    heur = 0
    rows,cols = np.shape(board)
    rows = rows-1
    # moves_left = cols + 2
    computer = 'x'
    player = 'o'
    if game_verison >= 4:
        moves_left = rows*cols
        for row in range(rows):
            for col in range(cols):
                #check horizontal entries and assigns value to heuristic
                try:
                    if board[row][col] == board[row][col+1] == 'o':
                        heur -=10
                    if board[row][col] == board[row][col+1] == 'x':
                        heur +=10
                    if board[row][col] == board[row][col+1] == board[row][col+2] =='o':
                        heur -=100
                    if board[row][col] == board[row][col+1] == board[row][col+2] =='x':
                        heur +=100
                    if board[row][col] == board[row][col+1] == board[row][col+2] == board[row][col+3] =='o':
                        heur -=10000
                    if board[row][col] == board[row][col+1] == board[row][col+2] == board[row][col+3] =='x':
                        heur +=10000
                except IndexError:
                        pass
    #             #check vertical entries and assigns value to heuristic
                try:
                    if board[row][col] == board[row+1][col] =='o':
                        heur -=10
                    if board[row][col] == board[row+1][col] =='x':
                        heur +=10
                    if board[row][col] == board[row+1][col] == board[row+2][col] =='o':
                        heur -=100
                    if board[row][col] == board[row+1][col] == board[row+2][col] =='x':
                        heur +=100
                    if board[row][col] == board[row+1][col]== board[row+2][col] == board[row+3][col] =='o':
                        heur -=10000
                    if board[row][col] == board[row+1][col]== board[row+2][col] == board[row+3][col] =='x':
                        heur +=10000
                except IndexError:
                        pass
    #             #check positive diagonal and assigns value to heuristic
                try:
                    if board[row][col] == board[row+1][col+1] =='o':
                        heur -=10
                    if board[row][col] == board[row+1][col+1] =='x':
                        heur +=10
                    if board[row][col] == board[row+1][col+1] == board[row+2][col+2] =='o':
                        heur -=100
                    if board[row][col] == board[row+1][col+1] == board[row+2][col+2] =='x':
                        heur +=100
                    if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] =='o':
                        heur -=10000
                    if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] =='x':
                        heur +=10000
                except IndexError:
                    pass
                #check negative diagonal and assigns value to heuristic
                #we are ignoring negative index values, because it will lead to false result
                try:
                    if col-1<0:
                        raise IndexError
                    else:
                        if board[row][col] == board[row+1][col-1] == 'o':
                            heur -=10
                        if board[row][col] == board[row+1][col-1] == 'x':
                            heur +=10
                    if col-1<0 or col-2<0:
                        raise IndexError
                    else:
                        if board[row][col] == board[row+1][col-1] == board[row+2][col-2] == 'o':
                            heur -=100
                        if board[row][col] == board[row+1][col-1] == board[row+2][col-2] == 'x':
                            heur +=100
                    if col-1<0 or col-2<0 or col-3<0:
                        raise IndexError
                    else:
                        if board[row][col] == board[row+1][col-1] == board[row+2][col-2] == board[row+3][col-3] == 'o':
                            heur -=10000
                        if board[row][col] == board[row+1][col-1] == board[row+2][col-2] == board[row+3][col-3] == 'x':
                            heur +=10000
                except IndexError:
                    pass
        return heur, moves_left
    if game_verison == 3:
        moves_left = 9
        for row in range(rows):
            for col in range(cols):
                #check horizontal entries and assigns value to heuristic
                try:
                    if board[row][col] == board[row][col+1] == 'o':
                        heur -= 10
                    if board[row][col] == board[row][col+1] == 'x':
                        heur += 10
                    if board[row][col] == board[row][col+1] == board[row][col+2] == 'o':
                        heur -= 100
                    if board[row][col] == board[row][col+1] == board[row][col+2] == 'x':
                        heur += 100
                    # if board[row][col] == board[row][col+1] == board[row][col+2] == board[row][col+3] == 'o':
                    #     heur -= 10000
                    # if board[row][col] == board[row][col+1] == board[row][col+2] == board[row][col+3] == 'x':
                    #     heur += 10000
                except IndexError:
                    pass
    #             #check vertical entries and assigns value to heuristic
                try:
                    if board[row][col] == board[row+1][col] == 'o':
                        heur -= 10
                    if board[row][col] == board[row+1][col] == 'x':
                        heur += 10
                    if board[row][col] == board[row+1][col] == board[row+2][col] == 'o':
                        heur -= 100
                    if board[row][col] == board[row+1][col] == board[row+2][col] == 'x':
                        heur += 100
                    # if board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col] == 'o':
                    #     heur -= 10000
                    # if board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col] == 'x':
                    #     heur += 10000
                except IndexError:
                    pass
    #             #check positive diagonal and assigns value to heuristic
                try:
                    if board[row][col] == board[row+1][col+1] == 'o':
                        heur -= 10
                    if board[row][col] == board[row+1][col+1] == 'x':
                        heur += 10
                    if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == 'o':
                        heur -= 100
                    if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == 'x':
                        heur += 100
                    # if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == 'o':
                    #     heur -= 10000
                    # if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == 'x':
                    #     heur += 10000
                except IndexError:
                    pass
                #check negative diagonal and assigns value to heuristic
                #we are ignoring negative index values, because it will lead to false result
                try:
                    if col-1 < 0:
                        raise IndexError
                    else:
                        if board[row][col] == board[row+1][col-1] == 'o':
                            heur -= 10
                        if board[row][col] == board[row+1][col-1] == 'x':
                            heur += 10
                    if col-1 < 0 or col-2 < 0:
                        raise IndexError
                    else:
                        if board[row][col] == board[row+1][col-1] == board[row+2][col-2] == 'o':
                            heur -= 100
                        if board[row][col] == board[row+1][col-1] == board[row+2][col-2] == 'x':
                            heur += 100
                    if col-1 < 0 or col-2 < 0 or col-3 < 0:
                        raise IndexError
                    else:
                        if board[row][col] == board[row+1][col-1] == board[row+2][col-2] == board[row+3][col-3] == 'o':
                            heur -= 10000
                        if board[row][col] == board[row+1][col-1] == board[row+2][col-2] == board[row+3][col-3] == 'x':
                            heur += 10000
                except IndexError:
                    pass
        return heur, moves_left
    if game_verison == 3:
        moves_left = 9
        for row in range(rows):
            for col in range(cols):
                #check horizontal entries and assigns value to heuristic
                try:
                    if board[row][col] == board[row][col+1] == 'o':
                        heur -= 10
                        moves_left += 1
                    if board[row][col] == board[row][col+1] == 'x':
                        heur += 10
                        moves_left -= 1
                    if board[row][col] == board[row][col+1] == board[row][col+2] == 'o':
                        heur -= 100
                        moves_left = np.Nan
                    if board[row][col] == board[row][col+1] == board[row][col+2] == 'x':
                        heur += 100
                        moves_left = 0
                    # if board[row][col] == board[row][col+1] == board[row][col+2] == board[row][col+3] == 'o':
                    #     heur -= 10000
                    # if board[row][col] == board[row][col+1] == board[row][col+2] == board[row][col+3] == 'x':
                    #     heur += 10000
                except IndexError:
                    pass
    #             #check vertical entries and assigns value to heuristic
                try:
                    if board[row][col] == board[row+1][col] == 'o':
                        heur -= 10
                        moves_left += 1
                    if board[row][col] == board[row+1][col] == 'x':
                        heur += 10
                        moves_left += 1
                    if board[row][col] == board[row+1][col] == board[row+2][col] == 'o':
                        heur -= 100
                        moves_left = np.Nan
                    if board[row][col] == board[row+1][col] == board[row+2][col] == 'x':
                        heur += 100
                        moves_left = 0
                    # if board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col] == 'o':
                    #     heur -= 10000
                    # if board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col] == 'x':
                    #     heur += 10000
                except IndexError:
                    pass
    #             #check positive diagonal and assigns value to heuristic
                try:
                    if board[row][col] == board[row+1][col+1] == 'o':
                        heur -= 10
                        moves_left += 1
                    if board[row][col] == board[row+1][col+1] == 'x':
                        heur += 10
                        moves_left += 1
                    if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == 'o':
                        heur -= 100
                        moves_left = np.Nan
                    if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == 'x':
                        heur += 100
                        moves_left = 0
                    # if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == 'o':
                    #     heur -= 10000
                    # if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == 'x':
                    #     heur += 10000
                except IndexError:
                    pass
                #check negative diagonal and assigns value to heuristic
                #we are ignoring negative index values, because it will lead to false result
                try:
                    if col-1 < 0:
                        raise IndexError
                    else:
                        if board[row][col] == board[row+1][col-1] == 'o':
                            heur -= 10
                            moves_left += 1
                        if board[row][col] == board[row+1][col-1] == 'x':
                            heur += 10
                            moves_left -= 1
                    if col-1 < 0 or col-2 < 0:
                        raise IndexError
                    else:
                        if board[row][col] == board[row+1][col-1] == board[row+2][col-2] == 'o':
                            heur -= 100
                            moves_left = np.Nan
                        if board[row][col] == board[row+1][col-1] == board[row+2][col-2] == 'x':
                            heur += 100
                            moves_left = 0
                    # if col-1 < 0 or col-2 < 0 or col-3 < 0:
                    #     raise IndexError
                    # else:
                    #     if board[row][col] == board[row+1][col-1] == board[row+2][col-2] == board[row+3][col-3] == 'o':
                    #         heur -= 10000
                    #     if board[row][col] == board[row+1][col-1] == board[row+2][col-2] == board[row+3][col-3] == 'x':
                    #         heur += 10000
                except IndexError:
                    pass
        return heur, moves_left
    if game_verison == 2:
        moves_left = 4
        for row in range(rows):
            for col in range(cols):
                #check horizontal entries and assigns value to heuristic
                try:
                    if board[row][col] == board[row][col+1] == 'o':
                        heur -= 10
                        moves_left = np.NaN
                    if board[row][col] == board[row][col+1] == 'x':
                        heur += 10
                        moves_left = 0
                    # if board[row][col] == board[row][col+1] == board[row][col+2] == 'o':
                    #     heur -= 100
                    # if board[row][col] == board[row][col+1] == board[row][col+2] == 'x':
                    #     heur += 100
                    # if board[row][col] == board[row][col+1] == board[row][col+2] == board[row][col+3] == 'o':
                    #     heur -= 10000
                    # if board[row][col] == board[row][col+1] == board[row][col+2] == board[row][col+3] == 'x':
                    #     heur += 10000
                except IndexError:
                    pass
    #             #check vertical entries and assigns value to heuristic
                try:
                    if board[row][col] == board[row+1][col] == 'o':
                        heur -= 10
                        moves_left = np.Nan
                    if board[row][col] == board[row+1][col] == 'x':
                        heur += 10
                        moves_left = 0
                    # if board[row][col] == board[row+1][col] == board[row+2][col] == 'o':
                    #     heur -= 100
                    # if board[row][col] == board[row+1][col] == board[row+2][col] == 'x':
                    #     heur += 100
                    # if board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col] == 'o':
                    #     heur -= 10000
                    # if board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col] == 'x':
                    #     heur += 10000
                except IndexError:
                    pass
    #             #check positive diagonal and assigns value to heuristic
                try:
                    if board[row][col] == board[row+1][col+1] == 'o':
                        heur -= 10
                        moves_left = np.Nan
                    if board[row][col] == board[row+1][col+1] == 'x':
                        heur += 10
                        moves_left = 0
                    # if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == 'o':
                    #     heur -= 100
                    # if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == 'x':
                    #     heur += 100
                    # if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == 'o':
                    #     heur -= 10000
                    # if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == 'x':
                    #     heur += 10000
                except IndexError:
                    pass
                #check negative diagonal and assigns value to heuristic
                #we are ignoring negative index values, because it will lead to false result
                try:
                    if col-1 < 0:
                        raise IndexError
                    else:
                        if board[row][col] == board[row+1][col-1] == 'o':
                            heur -= 10
                            moves_left = np.Nan
                        if board[row][col] == board[row+1][col-1] == 'x':
                            heur += 10
                            moves_left = 0
                #     if col-1 < 0 or col-2 < 0:
                #         raise IndexError
                #     else:
                #         if board[row][col] == board[row+1][col-1] == board[row+2][col-2] == 'o':
                #             heur -= 100
                #         if board[row][col] == board[row+1][col-1] == board[row+2][col-2] == 'x':
                #             heur += 100
                #     if col-1 < 0 or col-2 < 0 or col-3 < 0:
                #         raise IndexError
                #     else:
                #         if board[row][col] == board[row+1][col-1] == board[row+2][col-2] == board[row+3][col-3] == 'o':
                #             heur -= 10000
                #         if board[row][col] == board[row+1][col-1] == board[row+2][col-2] == board[row+3][col-3] == 'x':
                #             heur += 10000
                except IndexError:
                    pass
        return heur, moves_left



#minimax algorithm for computer bot player
def minimax(board_copy, element, index_req, max_depth, depth):
    global node_explored
    global node_print
    #increment node every time child is created
    node_explored += 1
    #if game is complete and one of player wins then return large utility value
    if check_game_status(board_copy):
        if check_win(board_copy,'x'):
            return 100000*(max_depth-depth)
        elif check_win(board_copy,'o'):
            return -100000*(max_depth-depth)
        else:
            return 0

    #when reaches the maximum depth return heuristic value
    if depth>max_depth:
        return eval_function(board_copy, game_verison)[0]

    node_value = []
    node_index = []

    #switching to the elements every time
    if element == 'x':
        nxt_element = 'o'
    else:
        nxt_element = 'x'

    for i in range(board.shape[1]):
        node_count = 0
        node_copy = np.copy(board_copy)
        node, placement = add_element(node_copy, i, element)
        node_key = create_key(node)
        for row in node:
            for item in row:
                if (item == b'x') or (item == b'o'):
                    node_count += 1
        node_print.append(node, node_count)
        
        #don't do recursive call if there is no placement of element
        if not placement:
            continue
        #recursive call of minimax function
        value = minimax(node,nxt_element,False,max_depth, depth+1)
        node_value.append(value)
        node_index.append(i)

    #if its computer bot then return maximum value of explored node else minimum value
    if element == 'x':
        final_value = max(node_value)
    else:
        final_value = min(node_value)
    if index_req:
        #print ("player bot utility: ", node_value)
        return node_index[node_value.index(final_value)]
    else:
        return final_value

#minimax algorithm with alpha beta pruning for computer bot player
def minimax_apha_beta_pruning(board_copy, element, alpha, beta, index_req, max_depth, depth, game_verison):
    global node_explored
    global node_print
    global node_value
    # global node_level
    #increment node every time child is created
    node_explored += 1
    #if game is complete and one of player wins then return large utility value
    if check_game_status(board_copy):
        if check_win(board_copy,'x', game_verison):
            return 100000*(float(max_depth)-float(depth))
        elif check_win(board_copy,'o', game_verison):
            return -100000*(float(max_depth)-float(depth))
        else:
            return 0
    #when reaches the maximum depth return heuristic value
    if int(depth)>int(max_depth):
        return eval_function(board_copy, game_verison)

    node_value = []
    node_index = None
    v=0
    #set very high initial valae to V
    if element == 'x':
        v = -1000000
    else:
        v = 1000000

    #switching to the elements
    if element == 'x':
        nxt_element = 'o'
    else:
        nxt_element = 'x'

    for i in range(board.shape[1]):
        node_count = 0
        node_copy = np.copy(board_copy)
        node, placement = add_element(node_copy, i, element)
        #node_key = create_key(node)
        for row in node:
            for item in row:
                if (item == b'x') or (item == b'o'):
                    node_count += 1
        node_print.append([node, node_count])
       
        #don't do recursive call if there is no placement of element
        if not placement:
            continue
        #recursive call of minimax function
        value = minimax_apha_beta_pruning(node,nxt_element,alpha, beta, False,max_depth, depth+1, game_verison)
        if index_req:
            node_value.append(value)
        #determine the min and max turn and find v, alpha and beta
        if element == 'x':
            if v < value:
                v = value
                node_index = i
            if v >= beta:
                if index_req:
                    #print ("player bot utility, v is greater than beta: ", node_value)
                    return node_index
                else:
                    return v
            alpha = max(alpha, v)
        else:
            if v > value:
                v = value
                node_index = i
            if v <= alpha:
                if index_req:
                    #print ("player bot utility, v is less than alpha: ", node_value)
                    return node_index
                else:
                    return v
            beta = min(beta, v)
    if index_req:
        #print ("player bot utility, at index: ", node_value)
        return node_index
    else:
        return v
            

# main
if __name__ == '__main__':
    #global variable to count number of node expanded
    global node_explored
    global player_human
    node_explored = 0
    node_level = int()
    node_print = []
    #default value for default board setting
    width = 7
    height = 5
    choice = 0
    search_level = 3
    game_verison = 4
    print("Default setting has board width = 7, height = 5, minimax with alpha beta, and search_depth is 3")
    select = input("Use default setting? y/n: ")
    # If user has not selected then ask user to enter game specification
    if select != 'y':
        width, height, choice, search_level, game_verison = get_user_input()
        # width, height, choice, search_level = 10, 5, 0
        if width>10 or width<1 or height>10 or height<1:
            print("You did not enter correct value, try again")

    board = create_board(width,height)
    print ("Welcome to minimax")
    print()

    #get object of player and bot
    player_human = C4_Player(board,'o')
    player_bot = C4_Bot(board, 'x',search_level,choice)

    #First move of game for computer bot

    first_move = input("who should play first? AI or Human? ")
    if first_move == "AI":
        board,comp_pos = initial_move(board)
    if first_move == "Human":
        player_human_play = True
    print (board)

    #making second move of player human
    player_human_play = True
    while True:
        if player_human_play:
            board, position = player_human.play_your_move()
            if check_win(board,player_human.element, game_verison):
                print ("player human is winner")
                print()
                break
        else:
            board, position = player_bot.play_your_move()
            if check_win(board,player_bot.element, game_verison):
                print ("computer bot is winner")
                print()
                break
        #if game board is full, no win , then declare a game as draw
        if check_game_status(board):
            print ("game is draw")
            print()
            break
        # toggle the player to play one on one
        player_human_play = not player_human_play
    #print(winning_strategy(node_print, width, height))
    print ("thanks for playing")
