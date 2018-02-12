
"""
Author: Patrick Addis.
"""

import mqtt_remote_method_calls as com
import robot_controller as robo

import ev3dev.ev3 as ev3
import time


COLOR_NAMES = ["None", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]


# This list is just a helper list if you ever want the string (for printing or speaking) from a color value.


class DataContainer(object):
    """ Helper class that might be useful to communicate between different callbacks."""

    def __init__(self):
        self.running = True

def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    # mqtt_client.connect_to_pc("35.194.247.175")  # Off campus IP address of a GCP broker
    robot.loop_forever()  # Calls a function that has a while True: loop within it to avoid letting the program end.

    print("--------------------------------------------")
    print(" Drive to the color")
    print("  Up button goes to Red")
    print("  Down button goes to Blue")
    print("  Left button goes to Black")
    print("  Right button goes to White")
    print("--------------------------------------------")
    ev3.Sound.speak("Drive to the color").wait()
    print("Press Back to exit this program.")

    robot = robo.Snatch3r()
    dc = DataContainer()

    # For our standard shutdown button.
    btn = ev3.Button()
    # done: 2. Uncomment the lines below to setup event handlers for these buttons.
    btn.on_up = lambda state: drive_to_color(state, robot, ev3.ColorSensor.COLOR_RED)
    btn.on_down = lambda state: drive_to_color(state, robot, ev3.ColorSensor.COLOR_BLUE)
    btn.on_left = lambda state: drive_to_color(state, robot, ev3.ColorSensor.COLOR_BLACK)
    btn.on_right = lambda state: drive_to_color(state, robot, ev3.ColorSensor.COLOR_WHITE)
    btn.on_backspace = lambda state: handle_shutdown(state, dc)

    while dc.running:
        btn.process()
        time.sleep(0.01)

    print("Goodbye!")
    ev3.Sound.speak("Goodbye").wait()


# ----------------------------------------------------------------------
# Event handlers
# ----------------------------------------------------------------------
def drive_to_color(button_state, robot, color_to_seek):
    """
    When the button_state is True (pressed), drives the robot forward until the desired color is detected.
    When the color_to_seek is detected the robot stops moving forward and speaks a message.

    Type hints:
      :type button_state: bool
      :type robot: robo.Snatch3r
      :type color_to_seek: int
    """
    if button_state:
        ev3.Sound.speak("Seeking " + COLOR_NAMES[color_to_seek]).wait()
        # done: 3. Implement the task as stated in this module's initial comment block
        # It is recommended that you add to your Snatch3r class's constructor the color_sensor, as shown
        #   self.color_sensor = ev3.ColorSensor()
        #   assert self.color_sensor
        # Then here you can use a command like robot.color_sensor.color to check the value
        while True:
            if color_to_seek != robot.color_sensor:
                robot.drive(500, 500)

                break

        # DONE: 4. Call over a TA or instructor to sign your team's checkoff sheet.
        #
        # Observations you should make, the instance variable robot.color_sensor.color is always updating
        # to the color seen and that value is given to you as an int.

        ev3.Sound.speak("Found " + COLOR_NAMES[color_to_seek]).wait()


def handle_shutdown(button_state, dc):
    """Exit the program."""
    if button_state:
        dc.running = False


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
