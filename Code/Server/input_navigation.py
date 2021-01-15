#!/usr/bin/python3
import argparse
import os
import platform
import sys

if platform.system() != 'Linux':
    print(f'The program does NOT run on {platform.system()}')
    print('It requires evdev which is only available for Linux')
    print('Exiting.')
    exit(1)

from evdev import InputDevice, categorize, ecodes
from Motor import *
from Buzzer import *


"""
https://core-electronics.com.au/tutorials/using-usb-and-bluetooth-controllers-with-python.html
https://python-evdev.readthedocs.io/en/latest/usage.html -- keyboard
$ python
Python 3.7.3 (default, Jul 25 2020, 13:03:44) 
[GCC 8.3.0] on linux
>>> from evdev import ecodes
>>> ecodes.KEY_A
30
>>> ecodes.KEY[103]
'KEY_UP'
"""

def main(args):
    """
    CLI program to navigate using a keyboard or controller
    ex:
    device /dev/input/event3, name "Dell Dell USB Keyboard", phys "usb-0000:01:00.0-1.1/input0"
    device /dev/input/event2, name "Logitech K400", phys "usb-0000:01:00.0-1.1/input2:1"
    device /dev/input/event1, name "Sony PLAYSTATION(R)3 Controller", phys "usb-0000:01:00.0-1.4/input0"
    device /dev/input/event0, name "Sony PLAYSTATION(R)3 Controller Motion Sensors", phys "usb-0000:01:00.0-1.4/input0"
    """
    cli = argparse.ArgumentParser(description="Navigate the Freenove robot with different inputs")
    cli.add_argument('-c', '--controller', action="store_true", help="use a gamepad controller for input")
    cli.add_argument('-k', '--keyboard', action="store_true", help="use the keyboard for input")
    cli.add_argument('-i', '--interactive', action="store_true", help="interactively select the input device")
    cli.add_argument('-d', '--debug', action="store_true", help="print debug output, use with '-i' to setup \
            a new device")
    cli.add_argument('-v', '--verbose', action="count", default=0, help="print verbose output, \
            allows counting of verbosity (-vvv)")

    if len(sys.argv) == 1:
        print()
        cli.print_help()
        print()
        exit(3)

    opts = cli.parse_args(args)
    debug = opts.debug
    verbose = opts.verbose
    interactive = opts.interactive
    if opts.keyboard:
        input_devices = ['Logitech K400', 'Dell Dell USB Keyboard']
    if opts.controller:
        input_devices = ['Sony PLAYSTATION(R)3 Controller', '8Bitdo Zero GamePad']

    input_dev = ''
    event_files = os.listdir('/dev/input/')
    for event in event_files:
        if 'event' in event:
            tmp = InputDevice(f'/dev/input/{event}')  # the keyboards and/or controllers
            if verbose >= 1 or interactive:
                print(f'Found: {tmp}')
 
            if interactive:
                answer = input("Would you like to use this input device?  (y/n)\n")
                if answer.lower() == 'yes' or answer.lower() == 'y':
                    input_dev = tmp
                    break
            else:
                for input_device in input_devices:
                    if input_device == tmp.name:
                        input_dev = tmp
                        print(f'Using {input_dev.name} for input')
                        break
   
    if not input_dev:
        print('No input match found. Exiting.')
        exit(1)

    if not debug:  # used for setting up a new device, skip definitions below
        # button code variables (add/change to suit your device)
        if 'Sony PLAYSTATION(R)3 Controller' == input_dev.name:
            aBtn = 305
            bBtn = 304
            xBtn = 307
            yBtn = 308
            
            up = 544
            down = 545
            left = 546
            right = 547
            
            select = 314
            start = 315
            PSBtn = enter = 316
            
            r1 = 311
            r2 = 313
            l1 = 310
            l2 = 312
            
            rjstick = 318
            ljstick = 317
        elif '8Bitdo Zero GamePad' == input_dev.name:
            aBtn = 34
            bBtn = 36
            xBtn = 35
            yBtn = 23
            
            up = 46
            down = 32
            left = 18
            right = 33
            
            start = 24
            select = 49
            
            l1 = 37
            r1 = 50
        elif 'Logitech K400' == input_dev.name or 'Dell Dell USB Keyboard' == input_dev.name:
            up = 103
            down = 108
            left = 105
            right = 106
        
            enter = 28
        else:
            print('No valid input device found. Exiting.')
            exit(1)
 
    PWM=Motor()
    buzzer = Buzzer()
    
    try:
        #evdev takes care of polling the controller in a loop
        for event in input_dev.read_loop():
            if event.type == ecodes.EV_KEY:  # filters by event type
                if verbose == 1 or debug:
                    print(event)

                if not debug:
                    if event.value == 0:
                        PWM.setMotorModel(0,0,0,0)
                        buzzer.run('0')
                    elif event.value == 1:
                        if event.code == up:
                            PWM.setMotorModel(2000,2000,2000,2000)      
                        elif event.code == down:
                            PWM.setMotorModel(-2000,-2000,-2000,-2000)
                        elif event.code == left:
                            PWM.setMotorModel(-2000,-2000,2000,2000)
                        elif event.code == right:
                            PWM.setMotorModel(2000,2000,-2000,-2000)
                        elif event.code == enter:
                            buzzer.run('1')
                        
            if verbose == 2:
                print(categorize(event))  # more verbose output
 
    except KeyboardInterrupt:
        print(' Exiting.')

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print(' Exiting.')

