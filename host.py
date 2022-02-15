import argparse
import sys

from read import *
from write import *
from go import *

from random_player import RandomPlayer
# from my_player3 import QLearner
# from my_player import PerfectPlayer
from minmax import AlphaBetaAgent

def play_game(player, go, N, moves, verbose, learn):
    # print("is called????")
    piece_type, previous_board, current_board = readInput(N)
    # go = GO(N, verbose)
    go.moves = go.moves + 1
    go.set_board(piece_type, previous_board, current_board)

    try:
        # print("move started")
        player.move()
        # print("move done")
        action, i, j = readOutput()
    except:
        print("output.txt not found or invalid format")
        go.state = "ENDED"
        if learn:
            player.learn(go, piece_type)
        # sys.exit(3 - piece_type)
        return 3 - piece_type
    # print(action, i, j, piece_type)
    if (action == "MOVE"):
        # print("action {}, {}".format(i, j))
        if (not go.place_stone(piece_type, i, j)):
            if verbose: print("Game has ended huhuhuhuh")
            if verbose: print("The winner is {}".format("X" if (3 - piece_type == 1) else "O"))
            go.state = "ENDED"
            if learn:
                player.learn(go, piece_type)
            # sys.exit(3 - piece_type)
            return 3 - piece_type
        go.died_stones = go.remove_died_stones(3 - piece_type)

    if (verbose):
        go.print_board()

    if (go.end_game(action)):
        go.state = "ENDED"
        # if verbose: print("learn now!!!!!")
        if learn:
            player.learn(go, piece_type)
        result = go.get_winner()
        if (verbose):
            print("Game has ended")
            if (result == 0):
                print("The game has tied")
            else:
                print("The winner is {}".format("X" if (result == 1) else "O"))
        # sys.exit(result)
        return result
    
    piece_type = switch_stone(piece_type)

    if (action == "PASS"):
        go.previous_board = go.current_board
    
    writeNextInput(piece_type, go.previous_board, go.current_board)
    # sys.exit(0)
    return 0

def switch_stone(piece_type):
    # print("AXEEEE", piece_type)
    return BLACK if piece_type == WHITE else WHITE

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", "-s", required = False, type = int, help = "Size of the board", default = 5)
    parser.add_argument("--moves", "-m", required = False, type = int, help = "Number of moves played", default = 0)
    parser.add_argument("--verbose", "-v", required = False, type = bool, help = "Explain steps", default = True)
    parser.add_argument("--learn", "-l", required = False, type = bool, help = "Learn Q-values", default = True)
    args = parser.parse_args()
    player1 = RandomPlayer()
    myplayer = AlphaBetaAgent()

    go = GO(5, True)
    p1stats = [0, 0, 0]
    p2stats = [0, 0, 0]

    battle(myplayer, player1, p2stats, go, 5, 25, False, False)
    battle(player1, myplayer, p1stats, go, 5, 25, False, False)
    

    resetInput()
    print(p1stats)
    p1Won = p1stats[1]
    p2Won = p1stats[2] + p1stats[0]
    print(p2stats)
    p1Won += p2stats[2] + p2stats[0]
    p2Won += p2stats[1]

    print("My player win % = {}".format(p2Won/(p1Won + p2Won)*100))

def battle(player1, player2, stats, go, size, iter, verbose, learn):
    verbose = True
    for i in range(iter):
        if verbose: print("===========================================")
        if verbose: print("Round {} black".format("ta" if isinstance(player1, RandomPlayer) else "myplayer"), i+1)
        go.init_board()
        resetInput()
        while(not go.end_game()):
            play_game(player1, go, size, 25, verbose, learn)
            # go.print_board()
            play_game(player2, go, size, 25, verbose, learn)
            # go.print_board()

        if verbose: print("===========================================")
        if verbose: print("Result ", i+1)
        # if verbose: print("Winner: ", go.get_winner())
        winner = player1 if go.get_winner() == 1 else player2
        if verbose: print("Winner: {}".format("ta" if isinstance(winner, RandomPlayer) else "myplayer"))
        stats[go.get_winner()] += 1
        if verbose: print("===========================================")

def resetInput():
    ip = str(1) + "\n"

    for i in range(10):
        for j in range(5):
            ip += str(0)
        ip += "\n"
    
    with open("/Users/shindeak/Desktop/561-AI/HW/HW-2/work/try/input.txt", "w") as file:
        file.write(ip[: -1])

if __name__ == "__main__":
    main()