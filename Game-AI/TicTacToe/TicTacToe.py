"""
Stefan Young
Tic Tac Toe Machine Learning
August 24, 2016
"""
#---------------------------IMPORTS--------------------------------------
from random import random
from pickle import load, dump, HIGHEST_PROTOCOL
#---------------------------GLOBAL VARIABLES-----------------------------
TRIALS = 1000000
INITIAL_PROB = 25
#------------------------------------------------------------------------
def main():
                #Used to create all possible game states for later training
    """
    board_states = generate_board_states()
    database = generate_database(board_states, INITIAL_PROB)
    with open('database.pkl', 'wb') as f:
        dump(database, f, HIGHEST_PROTOCOL)
    print(len(database)) ### Should be 4520 total boards
    """
    """
                #Load and fill probabilities of victory for every board state
    with open('database.pkl', 'rb') as f:
        database = load(f)
                #Play trial games to fill probabilities
    for i in range(TRIALS):
        play_training_game(database)
                #Save new database of proabilities
    with open('database.pkl', 'wb') as f:
        dump(database, f, HIGHEST_PROTOCOL)
    """
    with open('database.pkl', 'rb') as f:
        database = load(f)

    play_real_game(database)
#------------------------------------------------------------------------
def play_real_game(database):
    print('Welcome to TicTacToe!\n')
    play = True
    while play:
        turn = 0
        board = '---------'
        while (turn < 9):
            if (turn % 2 == 0):
                arg = "start"
                print ('Player\'s turn\n')
                print_board(board)
                while (not arg.isdigit()):
                    arg = input('Select a move (q to quit): \n')
                    if (arg == 'q'):
                        quit()
                move = int(arg)
                board = board[0:move] + 'X' + board[move + 1:]
                if (is_winner(board, 'X')):
                    print('Player is the winner!')
                    break
            else:
                move = select_best_move(database, board)
                board = board[:move] + 'O' + board[move + 1:]
                print('Computer\'s move')
                print_board(board)
                if (is_winner(board, 'O')):
                    print('Sorry, the Computer won')
                    break
            turn += 1
        print_board(board)
        if (turn == 9):
            print ('It\'s a draw!')
        play = True if input('Play again? y/n') == 'y' else False


#------------------------------------------------------------------------
def select_best_move(database, board):
    return database[board].index(max(database[board]))
#------------------------------------------------------------------------
def print_board(board):
    for i in range(3):
        for j in range(3):
            print (' {0} {1}'.format(3 * i + j if board[3*i+j] == '-' else board[3*i+j], '|' if j < 2 else ''), end = '')
        if (i < 2):
            print('\n-----------')
    print('\n')
#------------------------------------------------------------------------
def play_training_game(database):
    turn = 0
    board = '---------'
    move_list = []
    while True:
        if (is_winner(board, 'X')):
            update_database(database, move_list, 'X')
            break
        elif (is_winner(board, 'O')):
            update_database(database, move_list, 'O')
            break
        elif turn == 9:
            update_database(database, move_list, 'DRAW')
            break
        move_pos = choose_move(database[board])
        if turn % 2 == 0:
            player = 'X'
        else:
            player = 'O'
        move_list.append((board, move_pos))
        if move_pos == len(board) - 1:
            board = board[0:move_pos] + player
        else:
            board = board[0:move_pos] + player + board[move_pos+1:]
        turn += 1
#------------------------------------------------------------------------
def choose_move(probabilities):
    total = sum(probabilities)
    rand = random()
    weighted_probs = [probabilities[i] / total for i in range(9)]
    cum, index = weighted_probs[0], 0
    while cum < rand:
        index += 1
        cum += weighted_probs[index]
    return index
#------------------------------------------------------------------------
def update_database(database, move_list, winner):
    if (winner == 'X'):
        xval = 3
        oval = -1
    elif (winner == 'O'):
        xval = -1
        oval = 3
    else:
        xval = 1
        oval = 1
    for i in range(len(move_list)):
        board, pos = move_list[i]
        if (i % 2 == 0):
            database[board][pos] += xval
        else:
            database[board][pos] += oval
        if database[board][pos] < 1:
            database[board][pos] = 1
#------------------------------------------------------------------------
def is_winner(board, player):
    if board[0]==player and board[1]==player and board[2]==player or \
       board[3]==player and board[4]==player and board[5]==player or \
       board[6]==player and board[7]==player and board[8]==player or \
       board[0]==player and board[3]==player and board[6]==player or \
       board[1]==player and board[4]==player and board[7]==player or \
       board[2]==player and board[5]==player and board[8]==player or \
       board[0]==player and board[4]==player and board[8]==player or \
       board[2]==player and board[4]==player and board[6]==player:
        return True
    return False
#------------------------------------------------------------------------   
def generate_board_states():
    board_stack = []
    board_states = set()
    board_stack.append(('---------', 0))
    while (board_stack):
        board, turn = board_stack.pop()
        if (is_winner(board, 'X') or is_winner(board, 'O')):
            continue
        board_states.add(board)
        if (turn == 8):
            continue
        open_pos = [i for i, x in enumerate(board) if x == '-']
        if turn % 2 == 0:
            player = 'X'
        else:
            player = 'O'
        for pos in open_pos:
            if pos == 8:
                board_stack.append((board[0:pos] + player, turn + 1))
            else:
                board_stack.append((board[0:pos] + player + board[pos + 1:], turn + 1))
    return board_states
#------------------------------------------------------------------------   
def generate_database(board_states, init_prob):
    database = dict()
    for state in board_states:
        open_pos = set(i for i, x in enumerate(state) if x == '-')
        probabilities = [0]*9
        for i in open_pos:
            probabilities[i] = init_prob
        database[state] = probabilities
    return database
#--------------------------------------------------------------------------

if __name__ == '__main__':
    main()