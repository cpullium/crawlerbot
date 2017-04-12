# -*- coding: utf-8 -*-


import numpy as np
import serial
import time
import Q_Agent_Class
import threading

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

def SingleMove(str RoboCmd)
	print 'Sent:', RoboCmd
	print 'Waiting on motors...'
	ser.write(RoboCmd)
	ser.write('\n')            
	startTime = time.time()
	cmdTimout()
	
#Main while loop
while (not crawlerDone):
    if ser.inWaiting()>0:
        print ser.read(100)
		
    else:
		RoboCmd = raw_input('Enter Crawler Command>> ')
			
			
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
		
		else:
			SingleMove(RoboCmd)  
			