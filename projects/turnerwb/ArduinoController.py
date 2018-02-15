"""
Uses the Firmata protocol to communicate with an Arduino, based off of the blink sample code provided
with the PyFirmata library
Author: Wesley Turner: example code by Tino de Bruijn
"""
import pyfirmata
import serial

REDPIN = 12  # Use Pin 12 for Red Light
GREENPIN = 13  # Use Pin 13 for Green Light (13 is also bulletin, will blink on startup)

# Adjust that the port match your system, see samples below:
# On Linux: /dev/tty.usbserial-A6008rIF, /dev/ttyACM0,
# On Windows: \\.\COM1, \\.\COM2
PORT = '\\.\COM2'
e = NameError  # Defines an exception for later
# Tries to create a new board
try:
    board = pyfirmata.Arduino(PORT)
except serial.SerialException:  # If the serial port is not found, notify user, but allow to continue (for debug)
    print("Serial Port " + str(PORT) + " Not found")
    print("Print only Mode engaged")


def reset():
    """
    Resets the LEDs by turning them both off. If no board is found, does nothing.
    :return: None
    """
    try:
        board.digital[REDPIN].write(0)
        board.digital[GREENPIN].write(0)
    except e:
        pass


def green_light():
    """
    Turns green LED on and red LED off. If no board is found, only prints "Green Light!"
    :return: None
    """
    try:
        board.digital[REDPIN].write(0)
        board.digital[GREENPIN].write(1)
    except e:
        pass
    print("Green Light!")


def red_light():
    """
    Turns red LED on and green LED off. If no board is found, only prints "Red Light!"
    :return: None
    """
    try:
        board.digital[REDPIN].write(1)
        board.digital[GREENPIN].write(0)
    except e:
        pass
    print("Red Light!")
