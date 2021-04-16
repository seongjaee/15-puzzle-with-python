import pygame
import random, time

class Board:
    def __init__(self):
        temp = list(range(1,17))
        random.shuffle(temp)
        self.board = [temp[:4], temp[4:8], temp[8:12], temp[12:16]]
        
    # Check whether puzzle is solvable or not
    def check_solvable(self):
        flattened = [num for row in self.board for num in row]
        cnt = 0
        for idx, num in enumerate(flattened):
            if num != 16:
                cnt += sum([num>x for x in flattened[idx+1:]])
            else:
                cnt += idx//4+1
            
        if cnt%2 != 0:
            idx_14 = where_num(self.board, 14)
            idx_15 = where_num(self.board, 15)
            self.board[idx_14[0]][idx_14[1]] = 15
            self.board[idx_15[0]][idx_15[1]] = 14
        
    def shuffle(self):
        flattened = [num for row in self.board for num in row]
        random.shuffle(flattened)
        self.board = [flattened[:4], flattened[4:8], flattened[8:12], flattened[12:16]]
        self.check_solvable()

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
            
    # Check whether game over or not
    def is_clear(self):
        return self.board == [[4*i+1, 4*i+2, 4*i+3, 4*i+4] for i in range(0,4)]
            

class Block(pygame.sprite.Sprite):
    def __init__(self, num):
        pygame.sprite.Sprite.__init__(self)
        
        self.image =  pygame.image.load(path +f'img{num}.png')
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

# file path
sprite_path = './img/'
sound_path = './sound/'

# Initialize Board
brd = Board()
brd.check_solvable()

# Initialize pygame
pygame.init()

# FPS
clock = pygame.time.Clock()

# Screen
size = [300,400]
screen = pygame.display.set_mode(size)
screen.fill((40,10,70))

# Sound
move_sound = pygame.mixer.Sound(path + 'move.wav')
restart_sound = pygame.mixer.Sound(path + 'restart.wav')

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

playing = True
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
            
            # Restart the game
            elif event.key == pygame.K_SPACE:
                start_ticks = pygame.time.get_ticks()
                brd.shuffle()
        
    # Draw background
    screen.fill((40,10,70))
    
    # Draw blocks
    for block in block_list:
        screen.blit(block.image, block.get_pos())
                
    timer = timer_font.render(f'{(pygame.time.get_ticks() - start_ticks)/1000:.2f}', True, (200,200,200))
    screen.blit(timer, (240, 15))
    screen.blit(text, (60, 355))
    pygame.display.update()
    pygame.display.flip()
    
    if brd.is_clear():
        # Stop game and wait for event
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:        # Quit
                playing = False
                break
            elif event.type == pygame.KEYDOWN:   # Space bar -> Restart
                if event.key == pygame.K_SPACE:
                    start_ticks = pygame.time.get_ticks()
                    brd.shuffle()
                    break
