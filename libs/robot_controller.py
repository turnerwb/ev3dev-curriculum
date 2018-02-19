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
COLOR_NAMES = ["None", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""

    def __init__(self):
        # Motors
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        # Sensors
        self.touch_sensor = ev3.TouchSensor()
        self.beacon_seeker = ev3.BeaconSeeker(channel=4)
        self.pixy = ev3.Sensor(driver_name="pixy-lego")
        self.color_sensor = ev3.ColorSensor()
        self.ir_sensor = ev3.InfraredSensor()
        # Defined Constants
        self.MAX_SPEED = 900
        self.running = True

        assert self.pixy
        assert self.color_sensor
        assert self.ir_sensor
        assert self.touch_sensor

        assert self.left_motor
        assert self.right_motor
        assert self.arm_motor

    def drive_inches(self, distance_in, left_sp, right_sp):
        """
        Drives robot forward a given distance at a given speed
        :param distance_in:
        :param left_sp:
        :param right_sp:
        :return:
        """
        degrees_per_inch = 90
        motor_turns_needed_in_degrees = distance_in * degrees_per_inch
        self.left_motor.run_to_rel_pos(position_sp=motor_turns_needed_in_degrees, speed_sp= left_sp)
        self.right_motor.run_to_rel_pos(position_sp=motor_turns_needed_in_degrees, speed_sp= right_sp)
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
        """
        Runs calibration procedures on the arm
        :return:
        """
        self.arm_motor.run_forever(speed_sp=self.MAX_SPEED)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")

        arm_revolutions_for_full_range = 14.2
        self.arm_motor.run_to_rel_pos(position_sp=-arm_revolutions_for_full_range * 360)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)

        self.arm_motor.position = 0

    def arm_up(self):
        """
        Causes the arm to go up until it presses the touch sensor
        :return:
        """
        self.arm_motor.run_forever(speed_sp=self.MAX_SPEED)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")

    def arm_down(self):
        """
        Causes the arm to return to the down position
        :return:
        """
        self.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=self.MAX_SPEED)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.arm_motor.stop(stop_action="brake")

    def drive(self, motor_sp):
        """
        Makes both motors spin at provides speed until stopped
        :param motor_sp:
        :return:
        """
        self.right_motor.run_forever(speed_sp=motor_sp)
        self.left_motor.run_forever(speed_sp=motor_sp)

    def stop(self):
        """
        breaks both motors
        :return:
        """
        self.right_motor.stop(stop_action="brake")
        self.left_motor.stop(stop_action="brake")

    def shutdown(self):
        """
        Says goodbye, turns LEDs back to green, and stops both motors
        :return:
        """
        ev3.Sound.speak("Goodbye").wait()
        print(" Goodbye")
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        self.left_motor.stop()
        self.right_motor.stop()
        self.running = False

    def loop_forever(self):
        """
        Not recommended to be used, causes the robot to loop forever while waiting for input
        :return:
        """
        self.running = True
        while self.running:
            time.sleep(0.1)

    def seek_beacon(self):
        """
        Seeks and drives to a beacon on channel set in beacon_seeker object
        :return:
        """
        forward_speed = 300
        turn_speed = 100
        while not self.touch_sensor.is_pressed:
            current_heading = self.beacon_seeker.heading  # use the beacon_seeker heading
            current_distance = self.beacon_seeker.distance  # use the beacon_seeker distance
            if current_distance == -128:
                # If the IR Remote is not found just sit idle for this program until it is moved.
                self.drive(turn_speed, -turn_speed)
            else:
                if math.fabs(current_heading) < 2:
                    print("On the right heading. Distance: ", current_distance)
                    if current_distance > 3:
                        self.drive(forward_speed, forward_speed)
                    else:
                        time.sleep(1.2)
                        self.stop()
                        return True
                else:
                    if math.fabs(current_heading) < 10:
                        print("Adjusting heading: ", current_heading)
                    else:
                        print("Heading Extremely Far Off!!", current_heading)
                    if current_heading > 0:
                        self.drive(turn_speed, -turn_speed)
                    else:
                        self.drive(-turn_speed, turn_speed)
        print("Abandon ship!")
        self.stop()
        return False

    def is_running(self):
        """
        Checks to see if either of the drive motors are running. Returns true if either one is, false otherwise.
        :return:
        """
        if self.left_motor.is_running or self.right_motor.is_running:
            return True
        return False

    # def color_seek(self):
    #     color_to_seek = ev3.ColorSensor.COLOR_BLUE
    #     ev3.Sound.speak("Seeking " + COLOR_NAMES[color_to_seek]).wait()