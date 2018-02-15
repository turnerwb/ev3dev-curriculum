"""
EV3Controller.py:
Main component of Red Light/Green Light game on the EV3 end. Combines EV3Gamemaster.py and EV3Communications.py to
create a system to communicate with the PC and take input from the PIXY camera
Author: Wesley B. Turner
"""
import EV3Communications as Com
import time
import robot_controller as robo
import EV3Gamemaster as Game


def main():
    # Initialise objects
    robot = robo.Snatch3r()
    controller = Game.Gamemaster()
    coms = Com.EV3CommunicationSystem(robot)
    # Waits for user to choose difficulty
    while controller.difficulty is None:
        controller.set_difficulty(coms.difficulty)
    # While game is running and user hasn't quit
    while controller.running is True:
        scan(robot, controller, coms)
        if robot.is_running():
            update_progress(robot, controller, coms)
            time.sleep(.01)
        if not coms.running:
            break
        if robot.touch_sensor.is_pressed:
            coms.loss_protocol()
            break
    robot.shutdown()


def scan(robot, controller, coms):
    """
    Checks the PIXY camera for a change in colour of the light
    :param robot: Snatch3r robot
    :param controller: Gamemaster
    :param coms: EV3CommunicationSystem
    :return: None
    """
    if not robot.is_running():  # If the robot is not moving
        if coms.caught:  # If the robot has been caught cheating, lose the game
            controller.loss_protocol(robot, coms)
        robot.pixy.mode = 'SIG1'  # Check for green, if it is there, move
        if robot.pixy.value(3) > 0:
            controller.generate_random()
            robot.drive(controller.speed, controller.speed)
    else:  # If the robot is stopped
        robot.pixy.mode = 'SIG2'  # Check for red
        if robot.pixy.value(3) > 0:
            cheat = controller.can_cheat()  # See if robot can cheat, if it can do so
            if cheat:
                time.sleep(.1)
                coms.cheated = True  # Tell the communication system you cheated
                update_progress(robot, controller, coms, 10)
            else:
                coms.cheated = False
            robot.stop()  # Stop the robot


def update_progress(robot, controller, coms, update_value=1):
    """
    Updates the victory progress and progress bar on the PC end
    :param robot: Snatch3r robot
    :param controller: Gamemaster
    :param coms: EV3CommunicationSystem
    :param update_value: an integer by which to update the victory condition and progress bar
    :return:
    """
    controller.update_progress(update_value*controller.multiplier)  # Update Victory condition
    coms.update_progress(update_value*controller.multiplier)  # Update progress bar
    if controller.victory:  # if the robot has won
        if robot.is_running():  # If the robot made it on a green light, then win
            controller.victory_protocol(robot, coms)
        else:  # Else it cheated to win, give the user some time to call it out
            timeout = time.time() + 15
            while time.time() < timeout:
                if coms.caught:  # if the user called it out, it loses, else it wins
                    controller.loss_protocol(robot, coms)
            controller.victory_protocol(robot, coms)


main()
