import pygame
import random, os
from pathlib import Path
import Board
import where

# Change file directory
DIR = Path(__file__).parent.absolute()
DIR = f'{DIR}'.replace('\\','/')
os.chdir(DIR)

class Block(pygame.sprite.Sprite):
    def __init__(self, num):
        pygame.sprite.Sprite.__init__(self)
        self.image =  pygame.image.load(img_path +f'img{num}.png')
        self.rect = self.image.get_rect()
        self.num = num

    def get_pos(self):
        pos_y, pos_x = where.where_num(brd.board, self.num)
        pos_x = (60+pd)*pos_x + x_pd
        pos_y = (60+pd)*pos_y + y_pd
        return pos_x, pos_y


def draw_blocks():
    for block in block_list:
        screen.blit(block.image, block.get_pos())

def draw_timer_text():
    timer = timer_font.render(f'{(pygame.time.get_ticks() - start_ticks)/1000:.1f}', True, (200,200,200))
    screen.blit(timer, (230, 20))
    screen.blit(text, (0, 340))

def stop_game():
    global playing
    global start_ticks
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:        # Quit
            playing = False
            break

        elif event.type == pygame.KEYDOWN:   # Space bar -> Restart
            if event.key == pygame.K_SPACE:
                start_ticks = pygame.time.get_ticks()
                brd.shuffle()
                restart_sound.play()
                break

def action():
    global playing
    global start_ticks
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        
        elif event.type == pygame.KEYDOWN:
            # Move blocks
            if event.key == pygame.K_UP:
                if event.mod == 1:
                    brd.move(1)
                    brd.move(1)
                brd.move(1)
                move_sound.play()
                
            elif event.key == pygame.K_DOWN:
                if event.mod == 1:
                    brd.move(0)
                    brd.move(0)
                brd.move(0)
                move_sound.play()
                
            elif event.key == pygame.K_RIGHT:
                if event.mod == 1:
                    brd.move(3)
                    brd.move(3)
                brd.move(3)
                move_sound.play()
                
            elif event.key == pygame.K_LEFT:
                if event.mod == 1:
                    brd.move(2)
                    brd.move(2)
                brd.move(2)
                move_sound.play()
            
            # Restart the game
            elif event.key == pygame.K_SPACE:
                start_ticks = pygame.time.get_ticks()
                brd.shuffle()
                restart_sound.play()

# file path
img_path = './img/'
sound_path = './sound/'

# Initialize Board
brd = Board.Board()
brd.check_solvable()

# Initialize pygame
pygame.init()

# FPS
clock = pygame.time.Clock()

# Game title
pygame.display.set_caption("15-puzzle")

# Image
icon = pygame.image.load(img_path+'icon.png')
text = pygame.image.load(img_path+'text.png')
pygame.display.set_icon(icon)

# Screen
size = [300,400]
screen = pygame.display.set_mode(size)
screen.fill((40,10,70))

# Sound
move_sound = pygame.mixer.Sound(sound_path + 'move.wav')
restart_sound = pygame.mixer.Sound(sound_path + 'restart.wav')

# Font
timer_font = pygame.font.SysFont('calibri', 25)

# Padding
pd = 4
y_pd = 60
x_pd = 24

# Create block objects
block_list = [Block(n) for n in range(1, 17)]

start_ticks = pygame.time.get_ticks()
playing = True

# Game loop
while playing:
    clock.tick(60)
    action()

    # Draw
    screen.fill((40,10,70))
    draw_blocks()
    draw_timer_text()
    pygame.display.update()
    pygame.display.flip()
     
    if brd.is_clear(): # Stop game and wait for event
        stop_game()