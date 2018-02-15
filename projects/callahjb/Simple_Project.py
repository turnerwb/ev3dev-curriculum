import ev3dev.ev3 as ev3
import robot_controller as robo
import time

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com

# Potential values of the color_sensor.color property
#   ev3.ColorSensor.COLOR_NOCOLOR is the value 0
#   ev3.ColorSensor.COLOR_BLACK   is the value 1
#   ev3.ColorSensor.COLOR_BLUE    is the value 2
#   ev3.ColorSensor.COLOR_GREEN   is the value 3
#   ev3.ColorSensor.COLOR_YELLOW  is the value 4
#   ev3.ColorSensor.COLOR_RED     is the value 5
#   ev3.ColorSensor.COLOR_WHITE   is the value 6
#   ev3.ColorSensor.COLOR_BROWN   is the value 7


COLOR_NAMES = ["None", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]

# ----------------------------------------------------------------------
# Classes
# ----------------------------------------------------------------------


class DataContainer(object):

    def __init__(self):
        self.running = True


class Window(object):

    def __init__(self, canvas):
        self.canvas = canvas

# ----------------------------------------------------------------------
# Main Project
# ----------------------------------------------------------------------


def main():

    print("Testing project Code")
    ev3.Sound.speak(" Robot is on ")

    ev3.Leds.all_off()
    robot = robo.Snatch3r()
    dc = DataContainer()

# ----------------------------------------------------------------------
# Button Controllers
# ----------------------------------------------------------------------

    btn = ev3.Button()

    btn.on_up = lambda state: handle_up_button(state, robot, ev3.ColorSensor.COLOR_BLUE, ev3.ColorSensor.COLOR_RED)
    btn.on_down = lambda state: handle_down_button(state, robot, ev3.ColorSensor.COLOR_GREEN, ev3.ColorSensor.COLOR_RED)
    btn.on_left = lambda state: handle_left_button(state, robot, ev3.ColorSensor.COLOR_BLACK, ev3.ColorSensor.COLOR_RED)
    btn.on_right = lambda state: handle_right_button(state, robot,
                                                     ev3.ColorSensor.COLOR_WHITE, ev3.ColorSensor.COLOR_RED)
    btn.on_backspace = lambda state: handle_shutdown(state, dc)

    while dc.running:
        btn.process()
        time.sleep(0.01)

    print("Goodbye!")
    ev3.Sound.speak("Goodbye").wait()

# ----------------------------------------------------------------------
# Event handlers
# ----------------------------------------------------------------------


def handle_up_button(button_state, robot, color_to_seek, color_to_avoid):

    if button_state:
        ev3.Sound.speak(" Seeking a job ").wait()
        time.sleep(1)

        while color_to_seek != robot.color_sensor.color:
            robot.drive(200, 200)
            if robot.color_sensor.color == color_to_avoid:
                ev3.Sound.speak(" Go away ")
                robot.drive()

        robot.stop()
        ev3.Sound.speak("Found " + COLOR_NAMES[color_to_seek]).wait()
        time.sleep(1)


def handle_down_button(button_state, robot, color_to_seek, color_to_avoid):

    if button_state:
        ev3.Sound.speak(" Seeking a job ").wait()
        time.sleep(1)

        while color_to_seek != robot.color_sensor.color:
            robot.drive(200, 200)
            if robot.color_sensor.color == color_to_avoid:
                ev3.Sound.speak(" Go away ")
                robot.drive()

        robot.stop()
        ev3.Sound.speak("Found " + COLOR_NAMES[color_to_seek]).wait()
        time.sleep(1)


def handle_left_button(button_state, robot, color_to_seek, color_to_avoid):

        if button_state:
            ev3.Sound.speak(" Seeking a job ").wait()
            time.sleep(1)

            while color_to_seek != robot.color_sensor.color:
                robot.drive(200, 200)
                if robot.color_sensor.color == color_to_avoid:
                    ev3.Sound.speak(" Go away ")
                    robot.drive()

            robot.stop()
            ev3.Sound.speak("Found " + COLOR_NAMES[color_to_seek]).wait()
            time.sleep(1)


def handle_right_button(button_state, robot, color_to_seek, color_to_avoid):

    if button_state:
        ev3.Sound.speak(" Seeking a job ").wait()
        time.sleep(1)

        while color_to_seek != robot.color_sensor.color:
            robot.drive(200, 200)
            if robot.color_sensor.color == color_to_avoid:
                ev3.Sound.speak(" Go away ")
                robot.drive()

        robot.stop()
        ev3.Sound.speak("Found " + COLOR_NAMES[color_to_seek]).wait()
        time.sleep(1)


def handle_shutdown(button_state, dc):
    """Exit the program."""
    if button_state:
        dc.running = False


# ----------------------------------------------------------------------
# Tkinter Window
# ----------------------------------------------------------------------

    root = tkinter.Tk()
    root.title("Rose Hulman Hallways")

    frame = ttk.Frame(root, padding=10)
    frame.grid()

    instructions = " Run away from teachers / To be determined "
    label = ttk.Label(frame, text=instructions)
    label.grid(columnspan=2)

    canvas = tkinter.Canvas(frame, background="lightgray", width=800, height=500)
    canvas.grid(columnspan=2)

    # Make callbacks for the two buttons.
    clear_button = ttk.Button(frame, text="Clear")
    clear_button.grid(row=3, column=0)
    clear_button["command"] = lambda: clear(canvas)

    quit_button = ttk.Button(frame, text="Quit")
    quit_button.grid(row=3, column=1)
    quit_button["command"] = lambda: quit_program(mqtt_client)

    # Create an MQTT connection
    my_delegate = Window(canvas)
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect("draw", "draw")

    root.mainloop()


def clear(canvas):
    """Clears the canvas contents"""
    canvas.delete("all")


def quit_program(mqtt_client):
    """For best practice you should close the connection.  Nothing really "bad" happens if you
       forget to close the connection though. Still it seems wise to close it then exit."""
    if mqtt_client:
        mqtt_client.close()
    exit()
# ----------------------------------------------------------------------
# End of Code
# ----------------------------------------------------------------------


main()
