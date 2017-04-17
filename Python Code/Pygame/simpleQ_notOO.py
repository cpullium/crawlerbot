# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 09:50:30 2017

@author: Edmond
"""

#INCLUDES
############################################################################
Import numpy as np
############################################################################

#VARIABLES
############################################################################
#system configuration variables

Servo_Min_Angle = 0
Servo_Max_Angle = 60
Servo_0_Step = 15
Servo_1_Step = 15

#state, action, reward variables

Q = np.zeros(shape=(5,5,4))    #create Q map and initialize to 0
R = np.zeros(shape=(5,5,4))    #create R map and initialize to 0
S0 = 2                          #first state index. every state defined by S = [S0][S1]
S1 = 2                          #second state index
S0_next                         #placeholder for observed state after taking an action 
S1_next 
Action                          #tracks the most recent action taken

#define Q learning parameters

Epsilon = 0.1                   #set epsilon to be 0.1 i.e. 10% randomness
Alpha = 0.5                     #set alpha which is learning rate or step size
Gamma = 0.5                     #set gamma which is discount rate for expected return

#other variables

Encoder_Val=0 

############################################################################


#Q-learning loop
############################################################################
    Policy()                    #Determine Next Action
    Take_Action()               #Take Action and move into next state
    Observe_S()                 #State you arrived in and if it's valid                    
    update_R()                  #Update the Reward map with observed reward
    Update_Q()                  #Update Q map with observed experience
    S0 = S0_next                #move to next state
    S1 = S1_next 
    
############################################################################


#supporting functions which are used in main Q-learning loop
############################################################################
def Policy()
'''
    Description: Epsilon-greedy Policy function
    
    Status: ready for testbench. dependent on greedy and random functions
'''
    Epsilon_Compare = np.random.rand(1)  #give a random value between 0 and 1
    if Epsilon_Compare > epsilon         #determine if action is greedy
        greedy_action()   
    else                                 #if not greedy, act randomly
        random_action()
    return

############################################################################

def Greedy_Action()
'''
    Description: greedy action chooses the action associated with the highest Q value
    
    Status: Need Proper indexing of Q arrays (see arrows)
'''
    all_zeros_flag = 1                  #flag for starting conditions where all q values are 0
    q_max = -1024                       #intialize q_max to very low number

    for i in range(1,9)                 #cycle through actions for max
        if Q[S0][S1][i] != 0            #check for a non-zero <<<--------------
            all_zeros_flag = 0           
         

        if Q[S0][S1][i] > q_max         #<<<-----------------------------------
            q_max = Q[S0][S1][i]        #<<<-----------------------------------
            action = i 
         
     
    if all_zeros_flag == 1              #check for all zero condition
        Random_Action()  
    
    return

############################################################################

void Random_Action()  
'''
    Description: random action takes a random action
    
    Status: Ready For Testbench
'''
    action = np.random.randint(0,7)  #choose random action index
    
    return

############################################################################

void Take_Action()
'''
    Description: takes action selected and executes it on actual hardware system
    
    Status: Almost ready for test bench. Needs proper indexing of R matrix(See arrow)
'''
    if Action == 0:                   #adjusts next state according to selected action
        S0_next = S0 + 1 
        S1_next = S1 - 1 
    elif Action == 1:
        S0_next = S0 + 1 
        S1_next = S1 
    elif Action == 2:
        S0_next = S0 + 1 
        S1_next = S1 + 1 
    elif Action == 3:
        S0_next = S0 
        S1_next = S1 - 1 
    elif Action == 4:
        S0_next = S0 
        S1_next = S1 + 1 
    elif Action == 5:
        S0_next = S0 - 1 
        S1_next = S1 - 1 
    elif Action == 6:
        S0_next = S0 - 1 
        S1_next = S1 
    elif Action == 7:
        S0_next = S0 - 1 
        S1_next = S1 + 1 


    if S0_next < 0 || S1_next < 0:      #check for invalid actions
        S0_next = S0 
        S1_next = S1 
        R(S0)(S1)(Action) = -10         #<<<-----punish invalid action selection
    
    elif S0_next > 4 || S1_next > 4:
        S0_next = S0 
        S1_next = S1 
        R(S0)(S1)(Action) = -10         #<<<-----------------------------------
        
    return
    
############################################################################

def Observe_S()  
'''
    Description: Notes the current servo values and updates S0_next, S1_next
    Returns 1 if new state is in state table. Otherwise, it returns 0.
    
    Status: need to connect this information to PC via bluetooth/Wifi
    and to RPi via UART: http://www.elinux.org/Serial_port_programming
'''
                                        #get value for servo 1
                                        #get value for servo 2
    if Servo_Min_Angle <= Servo_0_angle <= Servo_Max_Angle \    #check that state is valid
        and Servo_Min_Angle <= Servo_1_angle <= Servo_Max_Angle\
        and Servo_0_Angle % Servo_0_Step == 0\ 
        and Servo_1_Angle % Servo_1_Step == 0                   #end of really long conditional
        
        S0_Next = Servo_0_Angle/Servo_0_Step
        S1_Next = Servo_1_angle/Servo_1_Step
        return 1
    else                                #else return 0
        S0_Next = 2
        S1_Next = 2
        return 0

############################################################################

void Update_R()  
'''
    Description: processes encoder value and updates R-value in R table
'''
    int Delta 
    if(S0_next == S0 && S1_next == S1)  
	    R[S0][S1][action] = -10 
        return    #check for invalid action taken     
    
    else        
        Delta = Encoder_Curr - Encoder_Val     #get current encoder value and subtracprevious value from it
                             #divide the change by 10 and keep only 1 sig fig
            R[S1][S2][action] = (R[S1][S2][action]+Enc_Val)/2  #make running average with existing reward
    
############################################################################

def Update_Q()
'''
 Description: performs Q update function
'''
    Q[S0, S1, action] = Q[S0, S1, action] + alpha*(R[S0, S1, action] + Q_Max(S0, S1)) 

############################################################################

def Write_Servos()
'''
    Description: writes servos according to S0 and S1
'''
            #write shoulder servo to S0_next
            #write elbow servo to S1_next

############################################################################

def Q_Max(int State_1, int State_2)
'''
    Description: finds max Q value in a given state
'''
    temp = Q[State_1, State_2, 0]
    for i in range(1,3):
        if Q[State_1, State_2, i]>temp:
                temp = Q[State_1, State_2, i]
    
            
        

############################################################################






