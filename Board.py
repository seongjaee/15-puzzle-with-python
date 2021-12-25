import random
import where

class Board:
    def __init__(self):
        temp = list(range(1,17))
        random.shuffle(temp)
        self.board = [temp[:4], temp[4:8], temp[8:12], temp[12:16]]
        
    # Check whether puzzle is solvable or not amd make board solvable
    def make_solvable(self):
        flattened = [num for row in self.board for num in row]
        cnt = 0
        for idx, num in enumerate(flattened):
            if num != 16:
                cnt += sum([num>x for x in flattened[idx+1:]])
            else:
                cnt += idx//4+1
            
        if cnt%2 != 0:
            idx_14 = where.where_num(self.board, 14)
            idx_15 = where.where_num(self.board, 15)
            self.board[idx_14[0]][idx_14[1]] = 15
            self.board[idx_15[0]][idx_15[1]] = 14
        
    def shuffle(self):
        flattened = [num for row in self.board for num in row]
        random.shuffle(flattened)
        self.board = [flattened[:4], flattened[4:8], flattened[8:12], flattened[12:16]]
        self.make_solvable()

    # Move the block
    def move(self, direction):
        y, x = where.where_num(self.board, 16)
        def move_down():
            if y != 0:
                temp = self.board[y-1][x]
                self.board[y][x] = temp
                self.board[y-1][x] = 16

        def move_up():
            if y != 3:
                temp = self.board[y+1][x]
                self.board[y][x] = temp
                self.board[y+1][x] = 16

        def move_right():
            if x != 3:
                temp = self.board[y][x+1]
                self.board[y][x] = temp
                self.board[y][x+1] = 16

        def move_left():
            if x != 0:
                temp = self.board[y][x-1]
                self.board[y][x] = temp
                self.board[y][x-1] = 16

        move_dict = {0: move_down, 1: move_up, 2: move_right, 3: move_left}
        move_dict[direction]()

        # if direction == 0 and y != 0:   # Down
        #     temp = self.board[y-1][x]
        #     self.board[y][x] = temp
        #     self.board[y-1][x] = 16
            
        # elif direction == 1 and y != 3: # Up
        #     temp = self.board[y+1][x]
        #     self.board[y][x] = temp
        #     self.board[y+1][x] = 16
            
        # elif direction == 2 and x != 3: # Right
        #     temp = self.board[y][x+1]
        #     self.board[y][x] = temp
        #     self.board[y][x+1] = 16
            
        # elif direction == 3 and x != 0: # Left
        #     temp = self.board[y][x-1]
        #     self.board[y][x] = temp
        #     self.board[y][x-1] = 16
            
    # Check whether game over or not
    def is_clear(self):
        return self.board == [[4*i + 1, 4*i + 2, 4*i + 3, 4*i + 4] for i in range(4)]

    
