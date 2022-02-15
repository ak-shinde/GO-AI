# Helper function to read the input given by game host
def readInput(N, input_file_name="/Users/shindeak/Desktop/561-AI/HW/HW-2/work/try/input.txt"):
    with open(input_file_name, "r") as file:
        lines = file.readlines()
        piece_type = int(lines[0]) # stone color

        previous_board = [ [0 for j in range(N)] for i in range(N) ]
        current_board = [ [0 for j in range(N)] for i in range(N) ]

        # fill the 2d arrays of previous and current board states
        for i in range(1, N + 1):
            for j in range(len(lines[i].rstrip('\n'))):
                previous_board[i - 1][j] = int(lines[i][j])

        for i in range(N + 1, 2 * N + 1):
            for j in range(len(lines[i].rstrip('\n'))):
                current_board[i - N - 1][j] = int(lines[i][j])

        return piece_type, previous_board, current_board

# Helper function to read the output given by game host
# Used only for local host gameplay
def readOutput(output_file_name="/Users/shindeak/Desktop/561-AI/HW/HW-2/work/try/output.txt"):
    with open(output_file_name, "r") as file:
        move = file.readline().strip().split(',')
        # print(move)
        if (move[0] == "PASS"):
            return "PASS", -1, -1

        return "MOVE", int(move[0]), int(move[1])