"""
Game of Rose Hulman - Collect 100 points to graduate
"""


import ev3dev.ev3 as ev3

import time
import robot_controller as robo
import mqtt_remote_method_calls as com
import random as random


class GameRobot(object):

    def __init__(self):

        self.robot = robo.Snatch3r()
        self.score = 0
        self.mqtt_client = com.MqttClient(self)
        self.mqtt_client.connect_to_pc("broker.mqttdashboard.com")
        self.robot.mqtt_client = self.mqtt_client
        self.running = True
        self.playing = False
        self.mqtt_client.send_message("score_change_display", [self.score])

    def my_loop_forever(self):

        while self.running:
            time.sleep(0.1)
            if self.robot.touch_sensor.is_pressed or self.score > 99:
                break
            if self.playing:
                self.robot.drive(400)
                time.sleep(.1)
                print("Selected Color", self.color_to_seek)

                time.sleep(.1)
                print("Robot sees", self.robot.color_sensor.color)
                if self.robot.color_sensor.color == self.color_to_seek and self.robot.ir_sensor.proximity > 20:
                    time.sleep(.1)
                    self.score = self.score + 20
                    self.mqtt_client.send_message("score_change_display", [self.score])
                    self.robot.drive_inches(-2, 200, 200)
                    ev3.Sound.speak("mmmmmmmmmmmmmmmmmm")
                    self.robot.drive_inches(3, 200, 200)
                    self.robot.turn_degrees(random.randint(1, 360), 300)
                    time.sleep(2)
                    self.robot.drive(400)

                    print("New Score", self.score)

                elif self.robot.color_sensor.color == ev3.ColorSensor.COLOR_RED and self.robot.ir_sensor.proximity > 20:

                    time.sleep(.1)
                    self.score = 0
                    self.mqtt_client.send_message("score_change_display", [self.score])

                    ev3.Sound.speak(" YOU LOSE ")
                    self.robot.turn_degrees(random.randint(270, 300), 900)
                    self.robot.turn_degrees(random.randint(270, 300), 900)
                    self.robot.turn_degrees(random.randint(270, 300), 900)

                    print("New Score", self.score)
                    time.sleep(2)
                    break

                elif self.robot.ir_sensor.proximity < 20:
                    self.robot.drive_inches(-5, 200, 200)
                    self.robot.turn_degrees(random.randint(175, 185), 300)
                    self.robot.drive(400)
                else:
                    self.robot.drive(400)


    def input_seek(self, color):

        self.playing = True
        self.color_to_seek = color

    def shutdown(self):

        self.running = False
        ev3.Sound.speak('').wait()
        self.robot.shutdown()


def main():

    print('Robot is ready')
    ev3.Sound.speak("Robot is ready")
    my_robot = GameRobot()

    my_robot.my_loop_forever()
    my_robot.shutdown()


main()