import pygame
import sys, random, time

class Board:
    def __init__(self):
        self.board = list(range(1,17))
        self.is_clear = False
    
    # Shuffle the board
    def shff_board(self):
        random.shuffle(self.board)
        
        if not (is_solvable(self.board)): # if not solvable, switch 14 and 15
            idx_14 = self.board.index(14)
            idx_15 = self.board.index(15)
            self.board[idx_14] = 15
            self.board[idx_15] = 14
            
        # Method for reshaping (16,0) list -> (4,4) list
        reshape = lambda x : [x[:4], x[4:8], x[8:12], x[12:16]]
        self.board = reshape(self.board)
        
    # Move the block
    def move(self, direction):
        y, x = where_num(self.board, 16)
        
        if direction == 0 and y != 0:   # Down
            temp = self.board[y-1][x]
            self.board[y][x] = temp
            self.board[y-1][x] = 16
            
        elif direction == 1 and y != 3: # Up
            temp = self.board[y+1][x]
            self.board[y][x] = temp
            self.board[y+1][x] = 16
            
        elif direction == 2 and x != 3: # Right
            temp = self.board[y][x+1]
            self.board[y][x] = temp
            self.board[y][x+1] = 16
            
        elif direction == 3 and x != 0: # Left
            temp = self.board[y][x-1]
            self.board[y][x] = temp
            self.board[y][x-1] = 16
            
    # Check whether game over or not and set self.is_clear
    def check_clear(self):
        if self.board == [[4*i+1, 4*i+2, 4*i+3, 4*i+4] for i in range(0,4)]:
            self.is_clear = True
        return self.is_clear


class Block(pygame.sprite.Sprite):
    def __init__(self, num):
        pygame.sprite.Sprite.__init__(self)
        
        self.image =  pygame.image.load(path +f'/img{num}.png')
        self.rect = self.image.get_rect()
        self.num = num

    def get_pos(self):
        pos_y, pos_x = where_num(brd.board, self.num)
        pos_x = (60+pd)*pos_x + x_pd
        pos_y = (60+pd)*pos_y + y_pd
        return pos_x, pos_y


# Find the location of input number
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
            
    return cnt%2 == 0 # True if solvable

def game_restart():
    start_ticks = pygame.time.get_ticks()
    brd.shff_board()    

# Sprite image path
path = 'C:/Users/Seong/JupyterNotebookDoc/pygame_basic'

# Initialize Board
brd = Board()
brd.shff_board()

# Initialize pygame
pygame.init()

# FPS
clock = pygame.time.Clock()

playing = True

# Screen
size = [300,400]
screen = pygame.display.set_mode(size)
screen.fill((40,10,70))

# Font
timer_font = pygame.font.SysFont("arial", 20)
text_font = pygame.font.SysFont("arial", 30)
text = text_font.render('Space to restart', True, (200,200,200))

# Padding
pd = 4
y_pd = 60
x_pd = 24

# Create block objects and draw
block_list = [Block(n) for n in range(1, 17)]

for block in block_list:
    screen.blit(block.image, block.get_pos())

start_ticks = pygame.time.get_ticks()

# Game loop
while playing:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        
        elif event.type == pygame.KEYDOWN:
            
            # Move blocks
            if event.key == pygame.K_UP:
                brd.move(1)
                
            elif event.key == pygame.K_DOWN:
                brd.move(0)
                
            elif event.key == pygame.K_RIGHT:
                brd.move(3)
                
            elif event.key == pygame.K_LEFT:
                brd.move(2)
                
            #elif event.key == pygame.K_SPACE:
            #    game_restart()
            
            if brd.check_clear():
                print('Clear!')
                playing = False
        
    screen.fill((40,10,70))
    # Draw
    for block in block_list:
        screen.blit(block.image, block.get_pos())
                
    timer = timer_font.render(f'{(pygame.time.get_ticks() - start_ticks)/1000:.2f}', True, (200,200,200))
    screen.blit(timer, (240, 15))
    # screen.blit(text, (60, 355))
    pygame.display.update()
    pygame.display.flip()
    
time.sleep(2)