# Helper function to write the input for sending it to the game host
def writeNextInput(piece_type, previous_board, current_board, input_file_name = "/Users/shindeak/Desktop/561-AI/HW/HW-2/work/try/input.txt"):
    ip = ""
    ip += str(piece_type) + "\n"

    for i in previous_board:
        for j in i:
            ip += str(j)
        ip += "\n"

    for i in current_board:
        for j in i:
            ip += str(j)
        ip += "\n"

    with open(input_file_name, "w") as file:
        file.write(ip[:-1])

# Helper function to write the output for sending it to the game host
def writeToOutput(result, output_file_name="/Users/shindeak/Desktop/561-AI/HW/HW-2/work/try/output.txt"):
    op = ""

    if (result == "PASS"):
        # print("write pass")
        op = "PASS"
    else:
        op += str(result[0]) + "," + str(result[1])

    with open(output_file_name, "w") as file:
        file.write(op)