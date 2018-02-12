import random as rand


class Gamemaster(object):

    def __init__(self):
        # TODO Test and decide on final speed values for difficulties
        self.EASY_SPEED = 100
        self.MEDIUM_SPEED = 500
        self.HARD_SPEED = 900
        # TODO Test and decide on final bounds for difficulties
        self.EASY_BOUND = 9
        self.MEDIUM_BOUND = 99
        self.HARD_BOUND = 999

        self.difficulty = None
        self.bound = None
        self.speed = None

        self.generated_int = None

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        if self.difficulty == "hard":
            self.bound = self.HARD_BOUND
            self.speed = self.HARD_SPEED
        elif self.difficulty == "medium":
            self.bound = self.MEDIUM_BOUND
            self.speed = self.MEDIUM_SPEED
        else:
            self.bound = self.EASY_BOUND
            self.speed = self.EASY_SPEED

    def generate_random(self):
        self.generated_int = rand.randint(0, self.bound)
