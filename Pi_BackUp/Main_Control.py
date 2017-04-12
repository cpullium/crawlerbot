#!/usr/bin/env python

import serial
import numpy as np
import Q_Agent_Class

# Define UART port for communication with OpenCM
ser = serial.Serial('/dev/ttyAMA0')
ser.baudrate = 115200

#hyperparameters
alpha   = 0.5
gamma   = 0.5
epsilon = 0.1

#define state space
Row_Num = 3
Col_Num = 3
Act_Num = 4

#initialize Q and R tables
Q = np.zeros((Row_Num, Col_Num, Act_Num))
R = np.random.random((Row_Num, Col_Num, Act_Num))

#initialize the learning agent
Q_Agent = Q_Agent_Class.Q_Agent_Class()

#Q algorithm loop
while 1: 
	Q_Agent.Policy(epsilon, Act_Num, Q)
	cmd = Q_Agent.Take_Action(Row_Num, Col_Num, Act_Num, R)
	ser.write(cmd)
	ser.flush()
	read = ser.read(1)
	Ans = int(read,16)
	print Ans
	if Ans & 0xA1:
		read = ser.read(1)
		Ans = int(read, 16)
		if Ans and 0xA2:
			print "great"
		elif Ans and 0xA3:
			print "oh no!"
		elif Ans and 0xA4:
			print "EPIC FAIL!"
		Reward = ser.read(1)
		if not (ser.read(1) and 0xAF):
			print "error: AF expected but not received"
	else: print "error: A1 expected but not received"
	Q_Agent.Q_Update(Q, alpha, gamma)

	#update state 
	Q_Agent.S0 = Q_Agent.S0_prime
	Q_Agent.S1 = Q_Agent.S1_prime


