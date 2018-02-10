"""
Uses the Firmata protocol to communicate with an Arduino, heavily based off of the blink sample code provided
with the PyFirmata library
Author: Wesley Turner, based off of code by Tino de Bruijn
"""
import pyfirmata
import serial

REDPIN = 12 # Use Pin 12 for Red Light
GREENPIN = 13
DELAY = 2 # A 2 seconds delay

# Adjust that the port match your system, see samples below:
# On Linux: /dev/tty.usbserial-A6008rIF, /dev/ttyACM0,
# On Windows: \\.\COM1, \\.\COM2
PORT = '\\.\COM2'
e = NameError
# Creates a new board
try:
    board = pyfirmata.Arduino(PORT)
except serial.SerialException:
    print("Serial Port " + str(PORT) + " Not found")
    print("Print only Mode engaged")


# Loop for blinking the led
# while True:
#     board.digital[REDPIN].write(1) # Set the LED pin to 1 (HIGH)
#     board.pass_time(DELAY)
#     board.digital[REDPIN].write(0) # Set the LED pin to 0 (LOW)
#     board.pass_time(DELAY)
#     board.digital[GREENPIN].write(1)
#     board.pass_time(DELAY)
#     board.digital[GREENPIN].write(0)
#     board.pass_time(DELAY)


def reset():
    try:
        board.digital[REDPIN].write(0)
        board.digital[GREENPIN].write(0)
    except :
        pass


def green_light():
    try:
        board.digital[REDPIN].write(0)
        board.digital[GREENPIN].write(1)
    except e:
        pass
    print("Green Light!")


def red_light():
    try:
        board.digital[REDPIN].write(1)
        board.digital[GREENPIN].write(0)
    except e:
        pass
    print("Red Light!")
