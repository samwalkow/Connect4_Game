import numpy as np
import operator
import time

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
        show_nodes = input("Show the game tree? y/n: ")
        if show_nodes == 'y':
            for node in node_print:
                node_level = 0
                print("node explored by computer bot:\n", node)
                for row in node[:-1]:
                    for item in row:
                        if item != b'.':
                            node_level +=1
                print("depth level:\n", node_level)
                if check_win(node, self.element, game_verison):
                    print("Outome: Winning Node - bot wins!")
                if check_win(node, player_human.element, game_verison):
                    print("Outcome: Losing Node - human wins")
                if not check_win(node, self.element, game_verison) and not check_win(node, player_human.element, game_verison):
                    print("Outcome: Unknown - game in progress")
                print()
            
        print()
        print ("Game board:\n", self.board)
        print ("\n\n")
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
    height = board.shape[0]-1
    width = int(board.shape[1]/2)
    board[height-1][width] = 'x'
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
    computer = 'x'
    player = 'o'
    if game_verison >= 4:
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
        return heur
    if game_verison == 3:
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
        return heur
    if game_verison == 3:
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
        return heur
    if game_verison == 2:
        for row in range(rows):
            for col in range(cols):
                #check horizontal entries and assigns value to heuristic
                try:
                    if board[row][col] == board[row][col+1] == 'o':
                        heur -= 10
                    if board[row][col] == board[row][col+1] == 'x':
                        heur += 10
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
                    if board[row][col] == board[row+1][col] == 'x':
                        heur += 10
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
                    if board[row][col] == board[row+1][col+1] == 'x':
                        heur += 10
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
        return heur



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
        return eval_function(board_copy)

    node_value = []
    node_index = []

    #switching to the elements every time
    if element == 'x':
        nxt_element = 'o'
    else:
        nxt_element = 'x'

    for i in range(board.shape[1]):
        node = np.copy(board_copy)
        node, placement = add_element(node,i,element)
        node_print.append(node)
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
        node = np.copy(board_copy)
        node, placement = add_element(node,i,element)
        node_print.append(node)
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
        # node_level = 2
    if first_move == "Human":
        player_human_play = True
        # node_level = 1
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
    print ("thanks for playing")
