import random
from read import readInput
from write import writeToOutput

from go import GO

class RandomPlayer():
    def __init__(self):
        self.type = 'random'

    def get_input(self, go, piece_type):
        # print("possible_placements ", piece_type, go.current_board)
        possible_placements = []
        for i in range(go.board_size):
            for j in range(go.board_size):
                # print("possible_placements {}, {}".format(i, j))
                if go.is_valid_move(i, j, piece_type):
                    possible_placements.append((i,j))

        # print("possible_placements ", possible_placements)
        if not possible_placements:
            # print("should pass now")
            return "PASS"
        else:
            return random.choice(possible_placements)
    
    def learn(self, go, piece_type):
        pass

    def move(self):
        N = 5
        # print("random choice: ", N)
        piece_type, previous_board, board = readInput(N)
        go = GO(N)
        go.set_board(piece_type, previous_board, board)
        # print("random choice: ", piece_type, board)
        action = self.get_input(go, piece_type)
        # print("random choice: ", action)
        writeToOutput(action)

if __name__ == "__main__":
    N = 5
    piece_type, previous_board, board = readInput(N)
    go = GO(N)
    go.set_board(piece_type, previous_board, board)
    player = RandomPlayer()
    action = player.get_input(go, piece_type)
    writeToOutput(action)