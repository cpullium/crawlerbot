# -*- coding: utf-8 -*-


import numpy as np
import serial
import time
import Q_Agent_Class
import threading
from string import Template

ser = serial.Serial('/dev/ttyAMA0',9600,timeout=0.2)
Q_Agent = Q_Agent_Class.Q_Agent_Class()

#hyperparameters
alpha = 0.5
gamma = 0.5
epsilon = .20

#Q table parameters
ROW_NUM = 3
COL_NUM = 3
ACT_NUM = 4 

#runFlag for Q_Agent
Q_runFlag = False
	
# Create a 3 dimensional array using the parameters 
Q = np.zeros((ROW_NUM, COL_NUM, ACT_NUM))
R = np.random.random((ROW_NUM, COL_NUM, ACT_NUM))

Q_Agent = Q_Agent_Class.Q_Agent_Class()
crawlerDone = False


#main Q algorithm
def RunQ():
	global Q_runFlag
	global Q
	
	while Q_runFlag:
		Q_Agent.Policy(epsilon, ACT_NUM, Q)
		Action = Q_Agent.Take_Action(ROW_NUM, COL_NUM, ACT_NUM)
		ser.write(Action)
		ser.write("\n")
		ser.flushInput()
		
		while(ser.inWaiting() == 0):
			continue
		
		message = ser.readline()
		print message
		if (message == "nothing\n") :
			Q_Agent.reward = -1
		elif (message == "positive\n"):
			Q_Agent.reward = 10
		elif (message == "negative\n"):
			Q_Agent.reward = -10
		else:
			Q_Agent.reward = 0
			print "Reward Error"
			
		print Q_Agent.reward	

#timeout for sending and receiving commands over UART
def cmdTimeout():
	while(time.time() - startTime < 3):
		if ser.inWaiting():
			break
		if time.time() - startTime > 2:
			print 'Command Timeout'
			break

#hard-coded walking sequence
def WorkingSequence():
	ser.write("right")
	ser.write('\n')            
	startTime = time.time()
	cmdTimeout()
	
	ser.write("right")
	ser.write('\n')            
	startTime = time.time()
	cmdTimeout()
	
	ser.write("right")
	ser.write('\n')            
	startTime = time.time()
	cmdTimeout()
	
	ser.write("down")
	ser.write('\n')            
	startTime = time.time()
	cmdTimeout()
	
	ser.write("left")
	ser.write('\n')            
	startTime = time.time()
	cmdTimout()
	
	ser.write("left")
	ser.write('\n')            
	startTime = time.time()
	cmdTimout()
	
	ser.write("left")
	ser.write('\n')            
	startTime = time.time()
	cmdTimout()
	
	ser.write("up")	
	ser.write('\n')            
	startTime = time.time()
	cmdTimout()

def SingleMove(RoboCmd):
	print 'Sent:', RoboCmd
	print 'Waiting on motors...'
	ser.write(RoboCmd)
	ser.write('\n')            
	startTime = time.time()
	cmdTimout()

#Checks if a string can represent a float (used in parsing)
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        print "Value must be a number."
        return False	

#Used for changing the value of epsilon. exampleCmd: Eps = .25
def checkForEpsilon(RoboCmd):
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
                print "Epsilon is now", epsilon
            else:
                print "Epsilon must be between 0 and 1"

#Used for changing the value of alpha. exampleCmd: alpha = .25				
def checkForAlpha(RoboCmd):
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
                print "Alpha is now", alpha
            else:
                print "Alpha must be between 0 and 1"				

#Used for changing the value of gamma. exampleCmd: gamma = .25				
def checkForGamma(RoboCmd):
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
                print "Gamma is now", gamma
            else:
                print "Gamma must be between 0 and 1"

#Displays current parameter values				
def showParams():
    print "Epsilon =", epsilon
    print "Alpha =", alpha
    print "Gamma =", gamma
	
#Main while loop
while (not crawlerDone):
    if ser.inWaiting()>0:
        print ser.read(100)
		
    else:
	    RoboCmd = raw_input('Enter Crawler Command>> ')
		
        checkForEpsilon(RoboCmd)
        checkForAlpha(RoboCmd)
        checkForGamma(RoboCmd)
			
        if RoboCmd == 'Run Q':
			if Q_runFlag == False:
				Q_runFlag = True	
				Qthread = threading.Thread(target = RunQ)
				Qthread.start()
				print "type 'Pause' to stop running Q"
			else:
				print 'Q is already running'
		
	    elif RoboCmd == 'Pause':
			Q_runFlag = False
		
		elif RoboCmd == 'Show Params':
			showParams()
		
		else:
			SingleMove(RoboCmd)  
			