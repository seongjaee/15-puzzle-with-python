# Find the location of input number
def where_num(board, num):
    for i in range(0,4):
        for j in range(0,4):
            if board[i][j] == num:
                return i, j