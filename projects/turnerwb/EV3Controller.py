import mqtt_remote_method_calls as com
import time
import robot_controller as robo
import Gamemaster as game

def main():
    robot = robo.Snatch3r()
    controller = game.Gamemaster()
    mqtt_client = com.MqttClient(controller)
    mqtt_client.connect_to_pc()
    while controller.running is True:
        scan(robot, controller, mqtt_client)
        if robot.is_running():
            update_progress(controller, mqtt_client)
            time.sleep(.01)


def scan(robot, controller, mqtt_client):
    if not robot.is_running():
        robot.pixy.mode = 'SIG1'
        if robot.pixy.value(3) > 0:
            controller.generate_random()
            robot.drive(controller.speed, controller.speed)
    else:
        robot.pixy.mode = 'SIG 2'
        if robot.pixy.value(3) > 0:
            cheat = controller.can_cheat()
            if cheat:
                time.sleep(.1)
                update_progress(robot, controller, mqtt_client, 10)
            robot.stop()


def update_progress(robot, controller, mqtt_client, update_value=1):
    mqtt_client.send_message("update_progress", [update_value])
    controller.update_progress(update_value)
    if robot.is_running():
        if controller.victory