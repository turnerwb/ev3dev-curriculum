import mqtt_remote_method_calls as com
import robot_controller as robo
import Gamemaster as game

def main():
    robot = robo.Snatch3r()
    controller = game.Gamemaster()
    mqtt_client = com.MqttClient(controller)
    is_green = False
    if not is_green:
        scan_green()


def scan_green(robot):
    robot.pixy.mode = 'SIG1'
    if robot.pixy.value(3):
        robot.drive(robot.MAX_SPEED, robot.MAX_SPEED)


def scan_red(robot):
    robot.pixy.mode = 'SIG 2'
