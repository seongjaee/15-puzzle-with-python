import random
import time

# Reshape (16,0) list -> (4,4) list
def reshape(board):
    return [board[:4],board[4:8],board[8:12],board[12:16]]

# Find the location of num
def where_num(board, num):
    for i in range(0,4):
        for j in range(0,4):
            if board[i][j] == num:
                return i,j
            
# Check the board whether solvable or not
def is_solvable(board):
    cnt = 0
    for idx, num in enumerate(board):
        if num != 16:
            cnt += sum([num>x for x in board[idx+1:]])
        else:
            cnt += (idx+1)//4+1
            
    return cnt % 2 == 0 # True if solvable
        
    
class Board:
    def __init__(self):
        self.board = list(range(1,17))
        self.control_loc = (0,0)
        self.is_clear = False
    
    # Shuffle the board
    def init_board(self):
        random.shuffle(self.board)
        if not (is_solvable(self.board)): # case not solvable, switch 14 and 15
            idx_14 = self.board.index(14)
            idx_15 = self.board.index(15)
            self.board[idx_14] = 15
            self.board[idx_15] = 14
        self.board = reshape(self.board)
        
    # find the location of blank
    def find_blank(self):
        self.control_loc = where_num(self.board, 16)
        
    # print current board, replace 16 to ' '
    def show_cur_board(self):
        f = lambda x: f'{x:>4}' if x!=16 else '    '
        print('\n\n'.join([' '.join(map(f, row)) for row in self.board]))
        
    # move the block
    def move(self, direction):
        self.find_blank()
        y, x = self.control_loc[0], self.control_loc[1]
        
        if direction == 'd' and y != 0:
            temp = self.board[y-1][x]
            self.board[y][x] = temp
            self.board[y-1][x] = 16
            
        elif direction == 'u' and y != 3:
            temp = self.board[y+1][x]
            self.board[y][x] = temp
            self.board[y+1][x] = 16
            
        elif direction == 'l' and x != 3:
            temp = self.board[y][x+1]
            self.board[y][x] = temp
            self.board[y][x+1] = 16
            
        elif direction == 'r' and x != 0:
            temp = self.board[y][x-1]
            self.board[y][x] = temp
            self.board[y][x-1] = 16
            
    def check_clear(self):
        if self.board == [[4*i+1, 4*i+2, 4*i+3, 4*i+4] for i in range(0,4)]:
            self.is_clear = True
            print('Clear!')
    

######### Game loop #########
b = Board()
b.init_board()
b.show_cur_board()
print('='*30)

while(not(b.is_clear)):
    direction = input("↑:'u', ↓:'d', →:'r', ←:'l'  ")
    if direction not in ('u', 'd', 'r', 'l'): break
    b.move(direction)
    b.show_cur_board()
    print('='*30)
    b.check_clear()
    
#############################

time.sleep(5)
