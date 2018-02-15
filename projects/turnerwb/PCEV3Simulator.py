"""
PCEV3Simulator.py:
Allows the user to simulate an EV3 robot on the PC for debugging. Not for use in the final project (i.e. This code is
contrived and in poor style, but will run without errors.)
Author: Wesley B. Turner
"""


import EV3Communications as com
import time
import fake_robot_controller as robo
import EV3Gamemaster as game
import TkinterWindow as Gui
green_width = 0
red_width = 0
robot = robo.Snatch3r()
controller = game.Gamemaster()
coms = com.EV3CommunicationSystem()


def main():
    global robot
    global controller
    global coms
    window = Gui.Window()
    window.green_button['command'] = lambda: set_green(robot, controller, coms)
    window.red_button['command'] = lambda: set_red(robot, controller, coms)
    window.cheat_button['command'] = lambda: update_protocol()
    while controller.difficulty is None:
        controller.set_difficulty(coms.difficulty)
    print(controller.difficulty)
    window.root.mainloop()

def update_protocol():
    global robot
    global controller
    global coms
    if robot.is_running():
        update_progress(robot, controller, coms)
        time.sleep(.01)


def scan(robot, controller, coms):
    global green_width
    global red_width
    if not robot.is_running():
        if coms.caught:
            controller.loss_protocol(robot, coms)
        # robot.pixy.mode = 'SIG1'
        if green_width > 0:
            controller.generate_random()
            robot.drive(controller.speed, controller.speed)
    else:
        # robot.pixy.mode = 'SIG 2'
        if red_width > 0:
            cheat = controller.can_cheat()
            if cheat:
                time.sleep(.1)
                coms.cheated = True
                update_progress(robot, controller, coms, 10)
            else:
                coms.cheated = False
            robot.stop()


def update_progress(robot, controller, coms, update_value=1):
    controller.update_progress(update_value)
    coms.update_progress(update_value)
    if controller.victory:
        if robot.is_running():
            controller.victory_protocol(robot, coms)
        else:
            timeout = time.time() + 15
            while time.time() < timeout:
                if coms.caught:
                    controller.loss_protocol(robot, coms)
            controller.victory_protocol(robot, coms)

def set_green(robot, controller, coms):
    global green_width
    global red_width
    green_width = 100
    red_width = 0
    scan(robot, controller, coms)

def set_red(robot, controller, coms):
    global green_width
    global red_width
    green_width = 0
    red_width = 100
    scan(robot, controller, coms)

main()