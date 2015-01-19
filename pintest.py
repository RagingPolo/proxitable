#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

def main():

    ## Tell the GPIO module that we are using it's numbering scheme
    GPIO.setmode(GPIO.BOARD)
    
    ## Setup GPIO pin ins
    GPIO.setup(26,GPIO.IN) ## Left button (1)
    GPIO.setup(23,GPIO.IN) ## Up button (2)
    GPIO.setup(21,GPIO.IN) ## Right button (3)
    GPIO.setup(18,GPIO.IN) ## Down button (4)
    GPIO.setup(15,GPIO.IN) ## Select button (5)
    GPIO.setup(12,GPIO.IN) ## Start button (6)
    GPIO.setup(10,GPIO.IN) ## B button (7)
    GPIO.setup(7,GPIO.IN) ## A button (8)

    ## Setup GPIO pin outs
    GPIO.setup(24,GPIO.OUT) ## Left button (1)
    GPIO.setup(22,GPIO.OUT) ## Up button (2)
    GPIO.setup(19,GPIO.OUT) ## Right button (3)
    GPIO.setup(16,GPIO.OUT) ## Down button (4)
    GPIO.setup(13,GPIO.OUT) ## Select button (5)
    GPIO.setup(11,GPIO.OUT) ## Start button (6)
    GPIO.setup(8,GPIO.OUT) ## B button (7)
    GPIO.setup(5,GPIO.OUT) ## A button (8)

    ## Set all GPIO pins to high
    GPIO.output(24,True) ## Left button (1)
    GPIO.output(22,True) ## Up button (2)
    GPIO.output(19,True) ## Right button (3)
    GPIO.output(16,True) ## Down button (4)
    GPIO.output(13,True) ## Select button (5)
    GPIO.output(11,True) ## Start button (6)
    GPIO.output(8,True) ## B button (7)
    GPIO.output(5,True) ## A button (8)

    ## while statement to constantly run, outputting various messages
    while True:
        if GPIO.input(26):
            print("Left button")
        elif GPIO.input(23):
            print("Up button")
        elif GPIO.input(21):
            print("Right button")
        elif GPIO.input(18):
            print("Down button")
        elif GPIO.input(15):
            print("Select button")
        elif GPIO.input(12):
            print("Start button")
        elif GPIO.input(10):
            print("B button")
        elif GPIO.input(7):
            print("A button")
        else:
            print("Naffin' mate!")

        ## Sleep before we move on
        time.sleep(0.01)


if __name__=="__main__":
    main()



## to run, make executable: "sudo chmod +x pins.py"
## then run: "sudo ./pins.py"
