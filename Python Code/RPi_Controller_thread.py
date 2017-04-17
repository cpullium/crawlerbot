# -*- coding: utf-8 -*-


import numpy as np
import serial
import time
import Q_Agent_Class
import threading

ser = serial.Serial('/dev/ttyAMA0',9600,timeout=0.2)
Q_Agent = Q_Agent_Class.Q_Agent_Class()

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
	
# Create a 3 dimensional array using the parameters 
Q = np.zeros((ROW_NUM, COL_NUM, ACT_NUM))
R = np.random.random((ROW_NUM, COL_NUM, ACT_NUM))

Q_Agent = Q_Agent_Class.Q_Agent_Class()
crawlerDone = False


#main Q algorithm
def RunQ():
	global Q_runFlag
	global Q_go
	global epsilon
	global alpha
	global gamma
	
	while Q_go:
		if Q_runFlag:
			
			Q_Agent.Policy(epsilon, ACT_NUM, Q)
			Action = Q_Agent.Take_Action(ROW_NUM, COL_NUM, ACT_NUM)
			if Action == 'out of bounds':
				print Action
			else:
				ser.write(Action)
				ser.write("\n")
				ser.flushInput()
				
				ser.flushOutput()
				while(ser.inWaiting() == 0):
					continue
				
				message = ser.readline()
#				print message
				if (message == "nothing\n") :
					Q_Agent.reward = -1
				elif (message == "positive\n"):
					Q_Agent.reward = 5
				elif (message == "negative\n"):
					Q_Agent.reward = -5
				else:
					Q_Agent.reward = 0
					print "Reward Error"	
#			print "State:%s%s            Action: %s       Reward = %s" %(Q_Agent.S0, Q_Agent.S1, Action, Q_Agent.reward)
			Q_Agent.Q_Update(Q, alpha, gamma)
			DrawQ()	
		else:
			continue

def DrawQ():
	for j in range(ROW_NUM):	
		#Up
		for i in range(0,COL_NUM):
			print "     |%s|     " %(round(Q[j][i][0],2)),
		print "\n"
		#Left and Right
		for i in range(0,COL_NUM):
			if Q_Agent.S0 == j and Q_Agent.S1 == i:
				print "|%s|  X  |%s|"%(round(Q[j][i][2],2),round(Q[j][i][3],2)),
			else:
				print "|%s|     |%s|"%(round(Q[j][i][2],2),round(Q[j][i][3],2)),
		print "\n"
		#down
		for i  in range(0,COL_NUM):
			print "     |%s|     " %(round(Q[j][i][1],2)),
		print "\n"
		
		print "--------------------------------------------------------------------------------"
		
#timeout for sending and receiving commands over UART
def cmdTimeout():
	startTime = time.time()
	while(time.time() - startTime < 2.1):
		if ser.inWaiting():
			break
		if time.time() - startTime > 2:
			print 'Command Timeout'
			break

#hard-coded walking sequence
def WorkingSequence():
	SingleMove("right")
	time.sleep(.25)
	SingleMove("right")
	time.sleep(.25)
	SingleMove("down")
	time.sleep(.25)
	SingleMove("left")
	time.sleep(.25)	
	SingleMove("left")
	time.sleep(.25)
	SingleMove("up")
	time.sleep(.25)

		
def SingleMove(RoboCmd):
	print 'Sent:', RoboCmd
	print 'Waiting on motors...'
	ser.write(RoboCmd)
	ser.write('\n')            
	cmdTimeout()

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
				print "Epsilon is now", epsilon
			else:
				print "Epsilon must be between 0 and 1"

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
				print "Alpha is now", alpha
			else:
				print "Alpha must be between 0 and 1"				

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
				print "Gamma is now", gamma
			else:
				print "Gamma must be between 0 and 1"

#Displays current parameter values				
def showParams():
    print "Epsilon =", epsilon
    print "Alpha =", alpha
    print "Gamma =", gamma
	
	
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
				Q_go = True
				Qthread = threading.Thread(target = RunQ)
				Qthread.start()
				print "type 'Pause' to stop running Q"
			else:
				print 'Q is already running'
			
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
			
