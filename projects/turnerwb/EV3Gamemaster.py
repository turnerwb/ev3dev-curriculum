"""
EV3Gamemaster.py:
Defines a class to handle random number generation and tracking of various game attributes such as difficulty and
progress towards victory
Author: Wesley B. Turner
"""
import random as rand


class Gamemaster(object):

    def __init__(self):

        self.EASY_SPEED = 100
        self.MEDIUM_SPEED = 500
        self.HARD_SPEED = 900

        self.EASY_BOUND = 9
        self.MEDIUM_BOUND = 99
        self.HARD_BOUND = 999

        self.difficulty = None
        self.bound = None
        self.speed = None
        self.multiplier = None

        self.generated_int = None

        self.victory = False
        self.VICTORY_RUNNING_TIME = 1000
        self.time = 0

        self.running = True

    def set_difficulty(self, difficulty):
        """
        Sets the game difficulty and appropriate speed and cheating frequency
        :param difficulty: a Str, either 'easy', 'medium', or 'hard'
        :return: None
        """
        self.difficulty = difficulty
        if self.difficulty is None:
            return None
        elif self.difficulty == "hard":
            self.bound = self.HARD_BOUND
            self.speed = self.HARD_SPEED
            self.multiplier = 10
        elif self.difficulty == "medium":
            self.bound = self.MEDIUM_BOUND
            self.speed = self.MEDIUM_SPEED
            self.multiplier = 5
        else:
            self.bound = self.EASY_BOUND
            self.speed = self.EASY_SPEED
            self.multiplier = 1

    def generate_random(self):
        """
        Generates a random Int and stores it
        :return: None
        """
        self.generated_int = rand.randint(0, self.bound)

    def can_cheat(self):
        """
        Check if robot is allowed to cheat. Returns True if generated int was zero, else returns False
        :return: True or False
        """
        if self.generated_int == 0:
            return True
        return False

    def update_progress(self, update_value=1):
        """
        Updates progress towards victory
        :param update_value: An int, usually one
        :return: None
        """
        self.time += update_value
        if self.time == self.VICTORY_RUNNING_TIME:
            self.victory = True

    def victory_protocol(self, robot, coms):
        """
        Declares victory for the robot and informs the user
        :param robot: A Snatch3r robot
        :param coms: EV3CommunicationSystem
        :return: None
        """
        robot.stop()
        coms.victory_protocol()
        self.running = False

    def loss_protocol(self, robot, coms):
        """
        Declares victory for the robot and informs the user
        :param robot: A Snatch3r robot
        :param coms: EV3CommunicationSystem
        :return: None
        """
        robot.stop()
        coms.loss_protocol()
        self.running = False
