from go import BLACK, BOARD_SIZE, GO
from read import readInput
from write import writeToOutput

class AlphaBetaAgent():

    def __init__(self):
        self.depth = 2  # Can increase to 3 but takes time with more branching factor
        self.color = BLACK

    # Return the best possible action based on current board state
    def get_input(self, board: GO, piece_type):
        self.color = piece_type
        # Pass if end game conditions are true or if the opponent passes and we are winning without making any move
        if board.end_game():
            return "PASS"
        if board.is_board_same(board.previous_board, board.current_board) and board.get_winner() == piece_type:
            return "PASS"
        
        score, actions = self.max_value(board, 0, float("-inf"), float("inf"))
        return actions[0] if len(actions) > 0 else "PASS"

    # Driver function for the host
    def move(self):
        # Initialise board from input given by host
        piece_type, previous_board, board = readInput(BOARD_SIZE)
        go = GO(BOARD_SIZE)
        go.set_board(piece_type, previous_board, board)

        # Get the best possible action using alpha-beta pruning
        action = self.get_input(go, piece_type)

        # Write the action to the output file
        writeToOutput(action)


    # Evaluate the score of board for a played move
    # We consider 6 hueristics:
    # 1. Difference between the number of my stones and opponent's stones
    # 2. Weight of the move - weights decrease as we move away from the centre of the board
    # 3. Euler number (Quad types) - these are special formations of stones in a 2x2 sub board which maximise the chances of capturing stones
    # 4. Minimising opponent's liberties
    # 5. Maximising our liberties
    # 6. Komi adjustment for white stones
    def eval(self, board: GO, piece_type):
        stone_score = board.get_score(self.color) - board.get_score(1 if self.color == 2 else 2)

        my_liberties = board.get_liberty_for(piece_type)
        opp_liberties = board.get_liberty_for(1 if self.color == 2 else 2)
        
        weight = board.board_weight(piece_type)

        euler = board.getEuler(piece_type)

        komi_adjustment = board.komi * (1 if self.color == 1 else -1)

        return 4 * stone_score + weight + 0.25 * euler - opp_liberties + 0.25 * my_liberties - 1.5 * komi_adjustment

    # Maximizer function to maximize our score
    def max_value(self, board:GO, depth, alpha, beta):
        if board.end_game() or depth == self.depth:
            return self.eval(board, self.color), []

        max_score = float("-inf")
        best_actions = []
        legal_actions = board.get_legal_actions(self.color)

        for action in legal_actions:
            # for each legal action, play move and check what the score is based on our eval function
            score, actions = self.min_value(board.play_chess(self.color, action[0], action[1]), depth, alpha, beta)
            if score > max_score:
                # for ever better score, we update the max score and actions
                max_score = score
                best_actions = [action] + actions

            # logic for alpha-beta pruning
            if max_score > beta:
                return max_score, best_actions
            if max_score > alpha:
                alpha = max_score

        return max_score, best_actions

    # Minimizer function to minimize opponent's score
    def min_value(self, board: GO, depth, alpha, beta):
        if board.end_game() or depth == self.depth:
            return self.eval(board, 1 if self.color == 2 else 2), []

        min_score = float("inf")
        worst_actions = []
        legal_actions = board.get_legal_actions(1 if self.color == 2 else 2)

        for action in legal_actions:
            # for each legal action, play move and check what the score is based on our eval function (for opponent)
            score, actions = self.max_value(board.play_chess(1 if self.color == 2 else 2, action[0], action[1]), depth+1, alpha, beta)
            if score < min_score:
                # for ever better score, we update the max score and actions
                min_score = score
                worst_actions = [action] + actions

            # logic for alpha-beta pruning
            if min_score < alpha:
                return min_score, worst_actions
            if min_score < beta:
                beta = min_score

        return min_score, worst_actions

# Main function used for local host game playing
if __name__ == "__main__":
    piece_type, previous_board, board = readInput(BOARD_SIZE)
    go = GO(BOARD_SIZE)
    go.set_board(piece_type, previous_board, board)
    player = AlphaBetaAgent()
    action = player.get_input(go, piece_type)
    writeToOutput(action)