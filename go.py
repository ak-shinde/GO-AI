from copy import deepcopy

WHITE, BLACK, EMPTY = 2, 1, 0
WHITE_VIS, BLACK_VIS, EMPTY_VIS = 'O', 'X', '.'
BOARD_SIZE = 5
GAME_END, IN_PROGRESS = 'END', 'IN_PROGRESS'

class GO:
    def __init__(self, N = BOARD_SIZE, verbose = False):
        self.board_size = N         # board size = 5
        self.moves = 0              # number of moves played till now
        self.verbose = verbose      # print logs for debugging
        self.max_moves = N * N - 1  # maximum number of moves allowed
        self.komi = N / 2           # komi for white stone
        self.died_stones = []       # keep track of dead stones after playing a move
        self.state = IN_PROGRESS    # whether the game has ended or is in progress

    # Initialize empty board
    def init_board(self):
        self.state = IN_PROGRESS
        self.moves = 0
        self.died_stones = []
        self.previous_board = [ [0 for j in range(self.board_size)] for i in range(self.board_size) ]
        self.current_board = [ [0 for j in range(self.board_size)] for i in range(self.board_size) ]

    # Set the board based on the input states given by host
    def set_board(self, piece_type, previous_board, current_board):
        self.previous_board = previous_board
        self.current_board = current_board

        for i in range(self.board_size):
            for j in range(self.board_size):
                # if our stones were captured by opponent, keep track of them
                if (previous_board[i][j] == piece_type and current_board[i][j] != piece_type):
                    self.died_stones.append((i, j))

    # Stringify the board in a 25 character string
    def encode_state(self):
        return ''.join([str(self.current_board[i][j]) for i in range(self.board_size) for j in range(self.board_size)])

    # Deep copy the entire board
    def copy_go(self):
        return deepcopy(self)

    # Update the current board
    def update_current_board(self, new_board):
        self.current_board = new_board

    # Check if the given 2 boards states are same or not
    def is_board_same(self, board1, board2):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if (board1[i][j] != board2[i][j]):
                    return False
        return True

    # Print the board - used for debugging purposes
    def print_board(self):
        print("-" * (self.board_size * 2 + 3))
        for i in range(self.board_size):
            row = "| "
            for j in range(self.board_size):
                if (self.current_board[i][j] == WHITE):
                    row += WHITE_VIS + " "
                elif (self.current_board[i][j] == BLACK):
                    row += BLACK_VIS + " "
                else:
                    row += EMPTY_VIS + " "
            print(row + "|")
        print("-" * (self.board_size * 2 + 3))

    # For a given row-column pair, find its immediate neighbours
    def get_neighbours(self, i, j):
        neighbours = []
        # check boundary conditions before adding neighbours
        if (i > 0):
            neighbours.append((i - 1, j))
        if (j > 0):
            neighbours.append((i, j - 1))
        if (i < self.board_size - 1):
            neighbours.append((i + 1, j))
        if (j < self.board_size - 1):
            neighbours.append((i, j + 1))
        return neighbours

    # Get group(same color stones) of niehgbour stones of a particular stone at i-j
    def detect_neighbor_ally(self, i, j):
        neighbors = self.get_neighbours(i, j)
        group_allies = []
        for piece in neighbors:
            if self.current_board[piece[0]][piece[1]] == self.current_board[i][j]:
                group_allies.append(piece)
        return group_allies

    # Play move - used for local host game play
    def place_stone(self, piece_type, i, j):
        if not self.is_valid_move(i, j, piece_type):
            self.state = GAME_END
            return False
        board = self.current_board
        self.previous_board = deepcopy(board)
        board[i][j] = piece_type

        self.update_current_board(board)
        return True

    # Play move and return the new board instance
    def play_chess(self, piece_type, i, j):
        if not self.is_valid_move(i, j, piece_type):
            self.state = GAME_END
            return self
        board = self.copy_go()
        board.previous_board = deepcopy(board.current_board)
        board.current_board[i][j] = piece_type
        # clear any dead(captured) stones
        board.died_stones = board.remove_died_stones(1 if piece_type == 2 else 2)
        return board

    # Get opponent's color
    def switch_stone(piece_type):
        return BLACK if piece_type == WHITE else WHITE

    # Get all possilbe valid actions for a stone color
    def get_legal_actions(self, piece_type):
        list = []
        for i in range(5):
            for j in range(5):
                if (self.is_valid_move(i,j,piece_type)):
                    list.append((i,j))
        return list

    # Check if a move is valid based on the give rules
    def is_valid_move(self, i, j, piece_type):
        # print("is_valid_move {}, {}".format(i, j))

        # Check boundary conditions of the board for i-j
        if (i < 0 or i >= self.board_size or j < 0 or j >= self.board_size):
            return False

        # Check is a stone is already placed at i-j
        if (self.current_board[i][j] != 0):
            return False

        # Make a deep copy for testing 
        test_go = self.copy_go()
        test_board = test_go.current_board

        # print("testgo ", i ,j, piece_type)
        # print("testgo ", test_board)
        test_board[i][j] = piece_type
        test_go.update_current_board(test_board)

        # After placing stone, if i-j has liberties, then its a valid move
        if (test_go.find_liberty(i, j)):
            return True

        # Killing opponent stones allows you to play stone even if there are no liberties for i-j
        test_go.remove_died_stones(3 - piece_type)
        # print("testgo ", test_board)
        if not test_go.find_liberty(i, j):
            return False
        else:
            # print("liberty true else block")
            # print(self.died_stones)
            # print(self.is_board_same(self.previous_board, test_go.current_board))

            # KO rule doesn't allow you to place the stone in the recently killed position
            if self.died_stones and self.is_board_same(self.previous_board, test_go.current_board):
                return False
        # print("true ", test_board)
        return True

    # Find the liberties for i-j position
    def find_liberty(self, i, j):
        # print("find_liberty", i,j)
        board = self.current_board
        # check ally groups of i-j
        ally_members = self.ally_dfs(i, j)
        for member in ally_members:
            # for every ally group, check their neighbouring liberties
            neighbors = self.get_neighbours(member[0], member[1])
            for piece in neighbors:
                if board[piece[0]][piece[1]] == 0:
                    # print("find_liberty true", i, j)
                    return True
        # print("find_liberty false", i, j)
        return False

    # Get the count of liberties for a stone color - used in eval function
    def get_liberty_for(self, piece_type):
        cnt = 0
        board = self.current_board
        for i in range(5):
            for j in range(5):
                if (piece_type == board[i][j]):
                    if (i > 0):
                        cnt += 1 if board[i-1][j] == 0 else 0
                    if (j > 0):
                        cnt += 1 if board[i][j-1] == 0 else 0
                    if (i < 4): 
                        cnt += 1 if board[i+1][j] == 0 else 0
                    if (j < 4): 
                        cnt += 1 if board[i][j+1] == 0 else 0
        return cnt


    # Get the liberty count of ally groups of i-j - not used currently in the eval function
    def ally_liberty(self, i, j):
        # print("find_liberty", i,j)
        board = self.current_board
        ally_members = self.ally_dfs(i, j)
        cnt = 0
        for member in ally_members:
            neighbors = self.get_neighbours(member[0], member[1])
            for piece in neighbors:
                if board[piece[0]][piece[1]] == 0:
                    cnt +=1
        return cnt
    
    # Number of stone of a given color on the edges of the board - not used currently in the eval function
    def numOnEdges(self, piece_type):
        cnt = 0
        for k in range(5):
            if(self.current_board[k][0] == piece_type):
                cnt += 1
            if(self.current_board[k][4] == piece_type):
                cnt += 1
            if(self.current_board[0][k] == piece_type):
                cnt += 1
            if(self.current_board[4][k] == piece_type):
                cnt += 1
        return cnt
    
    # Euler number of quad types of 2x2 sub board - used in eval function
    # q1 type:      01  10  00  00
    #               00  00  10  01
    # q2 type:      01  10  11  11
    #               11  11  10  01
    # q3 type:      01  10
    #               10  01
    def getEuler(self, piece_type):
        q1 = 0
        q2 = 0
        q3 = 0
        board = self.current_board
        for i in range(4):
            for j in range(4):
                if board[i][j]*board[i][j] + board[i+1][j]*board[i+1][j] + board[i][j+1]*board[i][j+1] + board[i+1][j+1]*board[i+1][j+1] == piece_type*piece_type:
                    q1 += 1
                if board[i][j]*board[i][j] + board[i+1][j]*board[i+1][j] + board[i][j+1]*board[i][j+1] + board[i+1][j+1]*board[i+1][j+1] == 3 * piece_type*piece_type:
                    q2 += 1
                if board[i][j]*board[i][j] + board[i+1][j+1]*board[i+1][j+1] == 0 and board[i][j+1]*board[i][j+1] + board[i+1][j]*board[i+1][j] == 2 * piece_type*piece_type:
                    q3 += 1
                if board[i+1][j] + board[i][j+1] == 0 and board[i][j]*board[i][j] + board[i+1][j+1]*board[i+1][j+1] == 2 * piece_type*piece_type:
                    q3 += 1
        return (q1 - q2 + q3)/4

    # Get the weight of the board
    # Central position (2-2) has weight 2
    # Edges has -2 weight
    # In between centre and edges each position has weight 1
    def board_weight(self, piece_type):
        cnt = 0
        for i in range(5):
            for j in range(5):
                if (self.current_board[i][j] == piece_type):
                    if i == j == 2:
                        cnt += 2
                    elif i == 0 or i == self.board_size - 1 or j == 0 or j == self.board_size - 1:
                        cnt += -2
                    else: cnt += 1
        return cnt

    # Run dfs on a position to find all ally groups(same color connected neighbours)
    def ally_dfs(self, i, j):
        stack = [(i, j)]
        ally_members = []
        while stack:
            piece = stack.pop()
            ally_members.append(piece)
            neighbor_allies = self.detect_neighbor_ally(piece[0], piece[1])
            # print("ally_dfs ", neighbor_allies)
            for ally in neighbor_allies:
                if ally not in stack and ally not in ally_members:
                    stack.append(ally)
        return ally_members

    # Find and remove the dead/captured stones from the board
    def remove_died_stones(self, piece_type):
        died_stones = self.find_died_pieces(piece_type)
        # print("remove_died_stones ", died_stones)
        if not died_stones:
            return []
        self.remove_stones(died_stones)
        return died_stones

    #  Remove the dead/captured stones from the board
    def remove_stones(self, died_stones):
        # print("remove_stones ", died_stones)
        for position in died_stones:
            self.current_board[position[0]][position[1]] = 0
        self.update_current_board(self.current_board)

    # Find the dead/captured stones from the board
    def find_died_pieces(self, piece_type):
        died_stones = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if (self.current_board[i][j] == piece_type and not self.find_liberty(i, j)):
                    died_stones.append((i, j))
        # print("find_died_pieces ", died_stones)
        return died_stones

    # Check conditions for terminating the game
    # NOTE: action is used only for local host game play
    def end_game(self, action = "MOVE"):
        if (self.state == GAME_END): # if somewhere in the game the end condition is achieved and state is set
            # print(self.state)
            return True
        if (self.moves == self.max_moves): # during minimax, check if we are playing more than 24 moves(max limit).
            # self.moves will always start from 0 for host as it creates a new board instance for every move of player
            # and there is no way to track the number of moves from input

            # print(self.moves)
            self.state = GAME_END
            # print(self.state + " " + str(self.max_moves))
            return True
        if self.is_board_same(self.previous_board, self.current_board) and action == "PASS":
            # if the board hasn't changed(Opponent passes) and the current move is also PASS then game ends
            self.state = GAME_END
            # print(self.state + " " + action)
            return True
        return False

    # Count the number of stones of a color on the board
    def get_score(self, piece_type):
        stone = 0
        for i in range(self.board_size):
            for j in range(self.board_size):
                if (self.current_board[i][j] == piece_type):
                    stone += 1
        return stone

    # Get the winner based on the max stones of a particular color on the board
    # We consider komi for white stones as well
    def get_winner(self):
        black_stones = self.get_score(BLACK)
        white_stones = self.get_score(WHITE)
        # draw condition is skipped here because with komi = 2.5, draw will never happen
        return BLACK if black_stones > white_stones + self.komi else WHITE
