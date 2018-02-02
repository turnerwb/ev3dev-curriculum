"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import math
import time


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""

    def __init__(self):
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()

        assert self.touch_sensor

    def drive_inches(self, distance_in, motor_sp):
        """
        Drives robot forward a given distance at a given speed
        :param distance_in:
        :param motor_sp:
        :return:
        """
        degrees_per_inch = 90
        motor_turns_needed_in_degrees = distance_in * degrees_per_inch
        self.left_motor.run_to_rel_pos(position_sp=motor_turns_needed_in_degrees, speed_sp=motor_sp)
        self.right_motor.run_to_rel_pos(position_sp=motor_turns_needed_in_degrees, speed_sp=motor_sp)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        """
        Turns robot a given angle at a given speed
        :param degrees_to_turn:
        :param turn_speed_sp:
        :return:
        """

        right_degrees_to_turn = 4.25*-degrees_to_turn
        left_degrees_to_turn = 4.25*degrees_to_turn
        self.left_motor.run_to_rel_pos(position_sp=right_degrees_to_turn, speed_sp=turn_speed_sp)
        self.right_motor.run_to_rel_pos(position_sp=left_degrees_to_turn, speed_sp=turn_speed_sp)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def arm_calibration(self):
        MAX_SPEED = 900
        self.arm_motor.run_forever(speed_sp=MAX_SPEED)
        while not self.touch_sensor:
            time.sleep(0.01)

        self.arm_motor.stop(stop_action="coast")

        arm_revolutions_for_full_range = 14.2
        self.arm_motor.run_to_rel_pos(position_sp=-arm_revolutions_for_full_range)
        self.arm_motor.wait_while(ev3.Motor.STATE_STALLED)

        self.arm_motor.position = 0  # Calibrate the down position as 0 (this line is correct as is).

    def arm_up(self):
        MAX_SPEED = 900
        self.arm_motor.run_to_rel_pos(position_sp=14.2, speed_sp=MAX_SPEED)
        while self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop()

    def arm_down(self):
        self.arm_motor.run_to_abs_pos()
        self.arm_motor.wait_while(ev3.Motor.STATE_HOLDING)

    def shutdown(self):
        ev3.Sound.speak("Goodbye").wait()
        print(" Goodbye")
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        self.left_motor.stop()
        self.right_motor.stop()