# -*- coding: utf-8 -*-



import serial
import time

ser = serial.Serial('/dev/ttyS0',9600,timeout=0.2)
crawlerDone = False

ser.flushInput();
while (not crawlerDone):
    if ser.inWaiting()>0:
        print ser.read(100)
    else:
        RoboCmd = raw_input('Enter Crawler Command>> ')
        if RoboCmd == 'done':
            print 'Exiting Program...'
            print 'Done'
            crawlerDone = True; 
        elif RoboCmd == 'up':
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
        else:
            ser.write(RoboCmd)
            ser.write('\n')
            print 'Sent:', RoboCmd
        time.sleep(.02)   
