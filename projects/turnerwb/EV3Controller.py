import EV3Communications as com
import time
import robot_controller as robo
import EV3Gamemaster as game

def main():
    robot = robo.Snatch3r()
    controller = game.Gamemaster()
    coms = com.EV3CommunicationSystem(controller)
    while controller.running is True:
        scan(robot, controller, coms)
        if robot.is_running():
            update_progress(controller, coms)
            time.sleep(.01)


def scan(robot, controller, coms):
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
                coms.cheated = True
                update_progress(robot, controller, coms, 10)
            robot.stop()


def update_progress(robot, controller, coms, update_value=1):
    coms.update_progress()
    controller.update_progress(update_value)
    if controller.victory:
        if robot.is_running():
            controller.victory_protocol()
        else:
            timeout = time.time() + 15
            while time.time() < timeout:
                pass
            controller.victory_protocol()
