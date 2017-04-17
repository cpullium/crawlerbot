# -*- coding: utf-8 -*-


import numpy as np
import serial
import time
import Q_Agent_Class

ser = serial.Serial('/dev/ttyAMA0',9600,timeout=0.2)
Q_Agent = Q_Agent_Class.Q_Agent_Class()

#hyperparameters
alpha = 0.5
gamma = 0.5
epsilon = .10

#Q table parameters
ROW_NUM = 3
COL_NUM = 3
ACT_NUM = 4 

# Create a 3 dimensional array using the parameters 
Q = np.zeros((ROW_NUM, COL_NUM, ACT_NUM))
R = np.random.random((ROW_NUM, COL_NUM, ACT_NUM))

Q_Agent = Q_Agent_Class.Q_Agent_Class()
crawlerDone = False
pause_flag = 1

ser.flushInput();
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
			q_flag = 1
			while True:
				if q_flag == 1:
					Q_Agent.Policy(epsilon, ACT_NUM, Q)
					Action = Q_Agent.Take_Action(ROW_NUM, COL_NUM, ACT_NUM, R)
					print Action
					ser.write(Action)
					ser.write('\n')
					q_flag==0
				if ser.inWaiting() == 0:
					print 'Waiting for Action to Complete'
				elif ser.inWaiting() > 0:
					if ser.read(100)=='success':
						ser.flushInput()
						q_flag = 1
					 R=10
				 Q_Agent.Q_Update(Q,alpha,gamma,R)

		else:
			ser.write(RoboCmd)
			ser.write('\n')
			print 'Sent:', RoboCmd
			time.sleep(.02)   
