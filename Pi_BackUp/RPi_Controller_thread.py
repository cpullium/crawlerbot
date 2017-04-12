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

def RunQ():
	global Q_runFlag
	global Q
	Q_runFlag == True
	
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

Qthread = threading.Thread(target = RunQ)

def WorkingSequence():
	ser.write("right")
	ser.write('\n')            
	startTime = time.time()
	while(time.time() - startTime < 3):
		if ser.inWaiting():
			break
		if time.time() - startTime > 2:
			print 'Command Timeout'
	ser.write("right")
	ser.write('\n')            
	startTime = time.time()
	while(time.time() - startTime < 3):
		if ser.inWaiting():
			break
		if time.time() - startTime > 2:
			print 'Command Timeout'
	ser.write("right")
	ser.write('\n')            
	startTime = time.time()
	while(time.time() - startTime < 3):
		if ser.inWaiting():
			break
		if time.time() - startTime > 2:
			print 'Command Timeout'
	ser.write("down")
	ser.write('\n')            
	startTime = time.time()
	while(time.time() - startTime < 3):
		if ser.inWaiting():
			break
		if time.time() - startTime > 2:
			print 'Command Timeout'
	ser.write("left")
	ser.write('\n')            
	startTime = time.time()
	while(time.time() - startTime < 3):
		if ser.inWaiting():
			break
		if time.time() - startTime > 2:
			print 'Command Timeout'
	ser.write("left")
	ser.write('\n')            
	startTime = time.time()
	while(time.time() - startTime < 3):
		if ser.inWaiting():
			break
		if time.time() - startTime > 2:
			print 'Command Timeout'
	ser.write("left")
	ser.write('\n')            
	startTime = time.time()
	while(time.time() - startTime < 3):
		if ser.inWaiting():
			break
		if time.time() - startTime > 2:
			print 'Command Timeout'
	ser.write("up")	
	ser.write('\n')            
	startTime = time.time()
	while(time.time() - startTime < 3):
		if ser.inWaiting():
			break
		if time.time() - startTime > 2:
			print 'Command Timeout'

while (not crawlerDone):
    if ser.inWaiting()>0:
        print ser.read(100)
		
    else:
		RoboCmd = raw_input('Enter Crawler Command>> ')
			
		if RoboCmd == 'up':
			print 'Sent:', RoboCmd
			print 'Waiting on motors...'
			ser.write(RoboCmd)
			ser.write('\n')            
			startTime = time.time()
			while(time.time() - startTime < 3):
				if ser.inWaiting():
					break
				if time.time() - startTime > 2:
					print 'Command Timeout'
						
		elif RoboCmd == 'down':
			print 'Sent:', RoboCmd
			print 'Waiting on motors...'
			ser.write(RoboCmd)
			ser.write('\n')            
			startTime = time.time()
			while(time.time() - startTime < 3):
				if ser.inWaiting():
					break
				if time.time() - startTime > 2:
					print 'Command Timeout'
						
		elif RoboCmd == 'left':
			print 'Sent:', RoboCmd
			print 'Waiting on motors...'
			ser.write(RoboCmd)
			ser.write('\n')            
			startTime = time.time()
			while(time.time() - startTime < 3):
				if ser.inWaiting():
					break
				if time.time() - startTime > 2:
					print 'Command Timeout'
					
		elif RoboCmd == 'right':
			print 'Sent:', RoboCmd
			print 'Waiting on motors...'
			ser.write(RoboCmd)
			ser.write('\n')            
			startTime = time.time()
			while(time.time() - startTime < 3):
				if ser.inWaiting():
					break
				if time.time() - startTime > 2:
					print 'Command Timeout'
			
		elif RoboCmd == 'Run Q':
			Qthread.start()
		
		elif RoboCmd == '-':
			epsilon == epsilon - 0.1
			print epsilon
			time.sleep(1)
		elif RoboCmd == '+':
			epsilon == epsilon + 0.1
			print epsilon
			time.sleep(1)
			
		elif RoboCmd == 'Pause':
			Q_runFlag = False
		
		else:
			ser.write(RoboCmd)
			ser.write('\n')
			print 'Sent:', RoboCmd
			time.sleep(.02)   
			