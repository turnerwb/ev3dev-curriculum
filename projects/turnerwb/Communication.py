"""
Communication.py:
Creates a class to communicate with the EV3 based off of inputs from the FinalProject.py, serves as MQTT Delegate to
receive messages from the EV3 as well
Author: Wesley B. Turner
"""

import mqtt_remote_method_calls as com


class CommunicationSystem(object):

    def __init__(self, window):
        self.mqtt_client = com.MqttClient(self)
        self.window = window
        self.mqtt_client.connect_to_ev3()

    def caught_cheating(self):
        """
        Sends message to EV3 to check if the robot cheated
        :return: None
        """
        print("J'Accuse!")
        self.mqtt_client.send_message('accused_cheating')

    def update_progress(self, update_amount):
        """
        Updates the progress bar on the user's screen to reflect the robot's status
        :param update_amount: Integer by which to move the progress bar
        :return: None
        """
        print("RECIEVING UPDATE PROGRESS")
        self.window.track += update_amount
        self.window.update_progress()

    def shutdown(self, early_exit=False):
        """
        Shuts down MQTT connection, if user quits the game before it's natural end, automatically causes user to lose
        :param early_exit: True only if user quits in the middle of a game
        :return:
        """
        print("Shutting down Coms")
        if early_exit:
            self.mqtt_client.send_message("victory_protocol", [])
        else:
            self.mqtt_client.close()

    def player_win(self):
        """
        Called by the EV3 to tell the user they have won
        :return: None
        """
        self.window.game_over(True)
        self.shutdown()
        try:
            self.window.root.destroy()
        except RuntimeError:
            pass

    def player_lose(self):
        """
        Called by the EV3 to tell the user they have lost
        :return: None
        """
        self.window.game_over(False)
        self.shutdown()
        self.window.root.destroy()

    def set_difficulty(self, difficulty):
        """
        Tells the EV3 what difficulty to play at
        :param difficulty: Str, either 'easy','medium', or 'hard'
        :return: None
        """
        self.mqtt_client.send_message("set_difficulty", [difficulty])

    @staticmethod
    def wrong_guess():
        """
        Called by the robot to inform the user that their accusation was wrong
        :return: None
        """
        print("Wrong! The robot didn't cheat")
