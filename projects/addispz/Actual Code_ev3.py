
"""
Author: Patrick Addis
"""

import mqtt_remote_method_calls as com
import robot_controller as robo

import ev3dev.ev3 as ev3
import time


# mqtt_client.connect_to_pc("35.194.247.175")  # Off campus IP address of a GCP broker


COLOR_NAMES = ["None", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]


class DataContainer(object):

    def __init__(self):
        self.running = True


dc = DataContainer()


def on_down(robot, mqtt_client):
    print(robot.is_running())
    while robot.is_running():
        drive_to_color(robot, ev3.ColorSensor.COLOR_BLUE, mqtt_client)


def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    ev3.Sound.speak("Drive to the color").wait()
    print("Press Back to exit this program.")

    btn = ev3.Button()
    btn.on_backspace = lambda state: handle_shutdown(state, dc)

    while dc.running:
        btn.process()
        time.sleep(0.01)
        on_down(robot, mqtt_client)

    print("Goodbye!")
    ev3.Sound.speak("Goodbye").wait()


# ----------------------------------------------------------------------
# Event handlers
# ----------------------------------------------------------------------
def drive_to_color(robot, color_to_seek, mqtt_client):
    """
    When the button_state is True (pressed), drives the robot forward until the desired color is detected.
    When the color_to_seek is detected the robot stops moving forward and speaks a message.

    Type hints:
      :type button_state: bool
      :type robot: robo.Snatch3r
      :type color_to_seek: int
    """
    ev3.Sound.speak("Seeking " + COLOR_NAMES[color_to_seek]).wait()
    while robot.is_running():
        if color_to_seek != robot.color_sensor.color:
            print('Not Found')
        else:
            robot.drive_inches(-6, 500)
            mqtt_client.send_message("pc_window", [])
            break
    robot.stop()

    ev3.Sound.speak("Found " + COLOR_NAMES[color_to_seek]).wait()


def handle_shutdown(button_state, dc):
    """Exit the program."""
    if button_state:
        dc.running = False


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
