# -*- coding: utf-8 -*-
"""
 Example program to show using an array to back a Q on-screen.
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
 Explanation video: http://youtu.be/mdTeqiWyFnc
"""
import pygame, sys
from pygame.locals import *
import numpy as np
import Q_Agent_Class
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

#hyperparameters
alpha = 0.5
gamma = 0.5
epsilon = .10

#Manual or automatic mode flag
Manual = True
 
# This sets the WIDTH and HEIGHT of each Q location

ROW_NUM = 3
COL_NUM = 3
ACT_NUM = 4 
# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
Q = np.zeros((ROW_NUM, COL_NUM, ACT_NUM))
R = np.random.random((ROW_NUM, COL_NUM, ACT_NUM))

Q_Agent = Q_Agent_Class.Q_Agent_Class()

# Initialize pygame
pygame.init()
pygame.font.init()
basicfont = pygame.font.SysFont(None,18)
# Set the WIDTH and HEIGHT of the screen
WINDOW_SIZE = [600, 600]
screen = pygame.display.set_mode(WINDOW_SIZE)
 
# Set title of screen
pygame.display.set_caption("Array Backed Q")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            Manual = not(Manual)
            
        elif event.type == pygame.KEYDOWN and Manual == True:
            if event.key == pygame.K_UP:
                Q_Agent.Next_Action = 0
                Q_Agent.Take_Action(ROW_NUM, COL_NUM, ACT_NUM, R)
            elif event.key == pygame.K_LEFT:
                Q_Agent.Next_Action = 1
                Q_Agent.Take_Action(ROW_NUM, COL_NUM, ACT_NUM, R)
            elif event.key == pygame.K_DOWN:
                Q_Agent.Next_Action = 2
                Q_Agent.Take_Action(ROW_NUM, COL_NUM, ACT_NUM, R)
            elif event.key == pygame.K_RIGHT:
                Q_Agent.Next_Action = 3
                Q_Agent.Take_Action(ROW_NUM, COL_NUM, ACT_NUM, R)
            Q_Agent.Q_Update(Q,alpha,gamma)
        elif event.type == pygame.KEYDOWN and Manual == False:
            if event.key == pygame.K_e: epsilon += round(.10,2)
            elif event.key == pygame.K_d: epsilon -= round(.10,2)
            if epsilon > 1: epsilon = 1
            if epsilon < 0: epsilon = 0
    if Manual == False:
         Q_Agent.Policy(epsilon, ACT_NUM, Q)
         Q_Agent.Take_Action(ROW_NUM, COL_NUM, ACT_NUM, R)
         Q_Agent.Q_Update(Q,alpha,gamma)

 
    # Set the screen background
    screen.fill(BLACK)
    WIDTH = (WINDOW_SIZE[0])/COL_NUM - 5
    HEIGHT = (WINDOW_SIZE[1])/ROW_NUM - 20
    
    #make button to toggle manual vs auto
    button_rect = pygame.Rect(50, (WINDOW_SIZE[1]-40), 100, 30)
    button = pygame.draw.rect(screen, GREEN, button_rect)
    if Manual:
        button_string = 'Go Full Auto!'
    else:
        button_string = 'epsilon = ' + str(round(epsilon, 2))
    textsurface = basicfont.render(button_string, False, WHITE)
    screen.blit(textsurface, (button_rect.left+10,button_rect.top+10))
    
    # Draw the Q
    for row in range(ROW_NUM):
        for column in range(COL_NUM):               
            temp = pygame.Rect((WIDTH * column + 5), (HEIGHT * row + 5),WIDTH,HEIGHT)
            
            #draw triangles for actions in each square
            Q_temp=Q[row][column]
            color = BLACK
            if Q_temp[0] > 0: color = (0,Q_temp[0]*COLOR_SCALE,0)
            elif Q_temp[0] < 0: color = (-Q_temp[0]*COLOR_SCALE,0,0)
            up = pygame.draw.polygon(screen,color,[(temp.topleft),(temp.topright),(temp.center)])
            color = BLACK            
            if Q_temp[3] > 0: color = (0,Q_temp[3]*COLOR_SCALE,0)
            elif Q_temp[3] < 0: color = (-Q_temp[3]*COLOR_SCALE,0,0)           
            right = pygame.draw.polygon(screen,color,[(temp.bottomright),(temp.topright),(temp.center)])
            color = BLACK
            if Q_temp[2] > 0: color = (0,Q_temp[2]*COLOR_SCALE,0)
            elif Q_temp[2] < 0: color = (-Q_temp[2]*COLOR_SCALE,0,0)
            down = pygame.draw.polygon(screen,color,[(temp.bottomleft),(temp.bottomright),(temp.center)])
            color = BLACK 
            if Q_temp[1] > 0: color = (0,Q_temp[1]*COLOR_SCALE,0)
            elif Q_temp[1] < 0: color = (-Q_temp[1]*COLOR_SCALE,0,0)
            left = pygame.draw.polygon(screen,color,[(temp.topleft),(temp.bottomleft),(temp.center)])            
            
            #draw white borders
            borders_int = pygame.draw.lines(screen,WHITE,False, [(temp.topleft),(temp.bottomright),(temp.topright),(temp.bottomleft)],4)
            borders_ext = pygame.draw.rect(screen, WHITE, (temp.left,temp.top,temp.width,temp.height),2)
            
            #place agent in square that was mode to
            if (Q_Agent.S0_prime == row) and (Q_Agent.S1_prime == column):
                Agent = pygame.draw.circle(screen, BLUE, temp.center, 20)
            
            Qup_string = str(round(Q[row][column][0],3))
            textsurface = basicfont.render(Qup_string, False, WHITE)
            screen.blit(textsurface, up.center)
            
            Qleft_string = str(round(Q[row][column][1],3))
            textsurface = basicfont.render(Qleft_string, False, WHITE)
            screen.blit(textsurface, left.center)
            
            Qdown_string = str(round(Q[row][column][2],3))
            textsurface = basicfont.render(Qdown_string, False, WHITE)
            screen.blit(textsurface, down.center)
            
            Qright_string = str(round(Q[row][column][3],3))
            textsurface = basicfont.render(Qright_string, False, WHITE)
            screen.blit(textsurface, right.center)
    # Limit to 60 frames per second
    clock.tick(60)
    
    Q_Agent.S0 = Q_Agent.S0_prime
    Q_Agent.S1 = Q_Agent.S1_prime
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()


