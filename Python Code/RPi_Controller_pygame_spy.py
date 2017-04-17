# -*- coding: utf-8 -*-

import pygame, sys
from pygame.locals import *
import numpy as np
import serial
import time
import Q_Agent_Class
import threading

#ser = serial.Serial('COM4',9600,timeout=0.2)
Q_Agent = Q_Agent_Class.Q_Agent_Class()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

#hyperparameters
alpha = 0.8
gamma = 0.8
epsilon = 0.9

#Q table parameters
ROW_NUM = 4
COL_NUM = 4
ACT_NUM = 4 

#runFlag for Q_Agent
Q_runFlag = False
Q_go = False
GUI_enabled = False
	
# Create a 3 dimensional array using the parameters 
Q = np.zeros((ROW_NUM, COL_NUM, ACT_NUM))
R = np.zeros((ROW_NUM, COL_NUM, ACT_NUM))

Q_Agent = Q_Agent_Class.Q_Agent_Class()
crawlerDone = False


#main Q algorithm
def RunQ():
    global Q_runFlag
    global Q_go
    global GUI_enabled
	
    global epsilon
    global alpha
    global gamma
	
    while Q_go:
        if Q_runFlag:
			
            Q_Agent.Policy(epsilon, ACT_NUM, Q)
            Action = Q_Agent.Take_Action(ROW_NUM, COL_NUM, ACT_NUM)
            if Action == 'out of bounds':
                print(Action)
            else:
                print(Action)
#                ser.write("\n")
#                ser.flushInput()
#                ser.flushOutput()
#				
#            while(ser.inWaiting() == 0):
#                continue
#					
#            message = ser.readline()
#				
#            if (message == "nothing\n") :
#                Q_Agent.reward = -1
#            elif (message == "positive\n"):
#                Q_Agent.reward = 5
#            elif (message == "negative\n"):
#                Q_Agent.reward = -5
#            else:
#                Q_Agent.reward = 0
#                print("Reward Error")	
            R[Q_Agent.S0][Q_Agent.S1][Action]=Q_Agent.reward
			
            Q_Agent.Q_Update(Q, alpha, gamma)
			
            if GUI_enabled:
                DrawQ()	
            else:
                continue
	
    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    if GUI_enabled:
        pygame.quit()

def DrawQ():
    global GUI_enabled
    global Q_go
    global Q
    global R
	
    if(GUI_enabled):
        if(Q_go):
            # Set the screen background
            screen.fill(BLACK)
            WIDTH = (WINDOW_SIZE[0])/COL_NUM - 5
            HEIGHT = (WINDOW_SIZE[1])/ROW_NUM - 20
            for row in range(ROW_NUM):
                for column in range(COL_NUM):               
                    temp = pygame.Rect((WIDTH * column + 5), (HEIGHT * row + 5),WIDTH,HEIGHT)
        					
                    #draw triangles for actions in each square
                    Q_temp=Q[row][column]
                    color = BLACK
                    if Q_temp[0] > 0: color = (0,Q_temp[0]*100,0)
                    elif Q_temp[0] < 0: color = (-Q_temp[0]*100,0,0)
                    up = pygame.draw.polygon(screen,color,[(temp.topleft),(temp.topright),(temp.center)])
                    color = BLACK            
                    if Q_temp[3] > 0: color = (0,Q_temp[3]*100,0)
                    elif Q_temp[3] < 0: color = (-Q_temp[3]*100,0,0)           
                    right = pygame.draw.polygon(screen,color,[(temp.bottomright),(temp.topright),(temp.center)])
                    color = BLACK
                    if Q_temp[2] > 0: color = (0,Q_temp[2]*100,0)
                    elif Q_temp[2] < 0: color = (-Q_temp[2]*100,0,0)
                    down = pygame.draw.polygon(screen,color,[(temp.bottomleft),(temp.bottomright),(temp.center)])
                    color = BLACK 
                    if Q_temp[1] > 0: color = (0,Q_temp[1]*100,0)
                    elif Q_temp[1] < 0: color = (-Q_temp[1]*100,0,0)
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
            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
		
#timeout for sending and receiving commands over UART
def cmdTimeout():
    startTime = time.time()
#    while(time.time() - startTime < 2.1):
#        if ser.inWaiting():
#            break
#        if time.time() - startTime > 2:
#            print('Command Timeout')
#            break

		
def SingleMove(RoboCmd):
    print('Sent:'), RoboCmd
    print('Waiting on motors...')
#    ser.write(RoboCmd)
#    ser.write('\n')            
#    cmdTimeout()

#Checks if a string can represent a float (used in parsing)
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        print("Value must be a number.")
        return False	

#Used for changing the value of epsilon. exampleCmd: Eps = .25
def checkForEpsilon(RoboCmd):
    global epsilon
	
    if(RoboCmd.find('Eps') > -1):
        RoboCmd = RoboCmd.replace("Eps", "eps")
    if(RoboCmd.find('epsilon') > -1):
        RoboCmd = RoboCmd.replace("epsilon", "eps")
    if(RoboCmd.find('eps =') > -1):
        RoboCmd = RoboCmd.replace("eps =", "eps=")
		
    StartIndex = RoboCmd.find('eps=')
    if StartIndex != -1:
        if is_number(RoboCmd[StartIndex+4:len(RoboCmd)]):
            tempEps = float(RoboCmd[StartIndex+4:len(RoboCmd)])
            if (tempEps >= 0 and tempEps <= 1):
                epsilon = tempEps
                print("Epsilon is now"), epsilon
            else:
                print("Epsilon must be between 0 and 1")

#Used for changing the value of alpha. exampleCmd: alpha = .25				
def checkForAlpha(RoboCmd):
    global alpha
	
    if(RoboCmd.find('Alpha') > -1):
        RoboCmd = RoboCmd.replace("Alpha", "alpha")
    if(RoboCmd.find('alpha =') > -1):
        RoboCmd = RoboCmd.replace("alpha =", "alpha=")
    StartIndex = RoboCmd.find('alpha=')
    if StartIndex != -1:
        if is_number(RoboCmd[StartIndex+6:len(RoboCmd)]):
            temp = float(RoboCmd[StartIndex+6:len(RoboCmd)])
            if (temp >= 0 and temp <= 1):
                alpha = temp
                print("Alpha is now %s") %(alpha)
            else:
                print ("Alpha must be between 0 and 1")				

#Used for changing the value of gamma. exampleCmd: gamma = .25				
def checkForGamma(RoboCmd):
    global gamma
	
    if(RoboCmd.find('Gamma') > -1):
        RoboCmd = RoboCmd.replace("Gamma", "gamma")
    if(RoboCmd.find('gamma =') > -1):
        RoboCmd = RoboCmd.replace("gamma =", "gamma=")
    StartIndex = RoboCmd.find('gamma=')
    if StartIndex != -1:
        if is_number(RoboCmd[StartIndex+6:len(RoboCmd)]):
            temp = float(RoboCmd[StartIndex+6:len(RoboCmd)])
            if (temp >= 0 and temp <= 1):
                gamma = temp
                print("Gamma is now"), gamma
            else:
                print("Gamma must be between 0 and 1")

#Displays current parameter values				
def showParams():
    print ("Epsilon ="), epsilon
    print ("Alpha ="), alpha
    print ("Gamma ="), gamma
		
while (not crawlerDone):
#    if ser.inWaiting()>0:
#        print (ser.read(100))
#		
#    else:
    RoboCmd = input('Enter Crawler Command>> ')
			
    checkForEpsilon(RoboCmd)
    checkForAlpha(RoboCmd)
    checkForGamma(RoboCmd)
				
    if RoboCmd == 'Run Q':
        if Q_runFlag == False:
            Q_runFlag = True	
            Q_go = True
            Qthread = threading.Thread(target = RunQ)
            Qthread.start()
            print ("type 'Pause' to stop running Q")
        else:
            print ('Q is already running')
				
    elif RoboCmd == 'gui on':
        GUI_enabled = True
			
    elif RoboCmd == 'Pause':
        Q_runFlag = False
		
    elif RoboCmd == 'Resume':
        Q_runFlag = True
		
    elif RoboCmd == 'Finish':
        Q_go = False
			
    elif RoboCmd == 'Show Params':
        showParams()
			
    elif RoboCmd == 'Show Q':
        DrawQ()
			
    else:
        SingleMove(RoboCmd)  
			
