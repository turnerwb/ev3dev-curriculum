import mqtt_remote_method_calls as com
import robot_controller as robo
import Gamemaster as game

def main():
    robot = robo.Snatch3r()
    controller = game.Gamemaster()
    mqtt_client = com.MqttClient(controller)
    is_green = False
    if not is_green:
        scan_green(robot, controller)
    else:
        scan_red(robot, controller)


def scan_green(robot, controller):
    robot.pixy.mode = 'SIG1'
    if robot.pixy.value(3) > 0:
        controller.generate_random()
        robot.drive(controller.speed, controller.speed)


def scan_red(robot, controller):
    robot.pixy.mode = 'SIG 2'
    if robot.pixy.value(3) > 0:
        controller.generated_int