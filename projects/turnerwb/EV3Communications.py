"""
EV3Communications.py:
Creates an object to handle the EV3 end of MQTT. Sends messages back to PC and serves as the EV3's MQTT Delegate
Author: Wesley B. Turner
"""

import mqtt_remote_method_calls as Com


class EV3CommunicationSystem(object):

    def __init__(self, robot):
        self.mqtt_client = Com.MqttClient(self)
        self.mqtt_client.connect_to_pc()
        self.cheated = False
        self.caught = False
        self.difficulty = None
        self.running = True
        self.robot = robot

    def update_progress(self, update_amount):
        """
        Informs the PC that the robot is moving and tells it to update the progress bar accordingly
        :param update_amount: Int, telling the computer how far the robot has moved
        :return: None
        """
        print("SENDING UPDATE PROGRESS")
        self.mqtt_client.send_message("update_progress", [update_amount])

    def shutdown(self):
        """
        Closes EV3's MQTT client
        :return: None
        """
        print("Shutting down Coms")
        self.mqtt_client.close()
        self.running = False

    def accused_cheating(self):
        """
        Called by PC to check if the robot has cheated, if true, sets an instance variable to tell the rest of the
        program that it has been caught
        :return: None
        """
        if self.cheated:
            self.caught = True
            print("Cheated")
        else:
            self.mqtt_client.send_message("wrong_guess", [])
            print("No Cheat")

    def victory_protocol(self):
        """
        Informs the user they have lost
        :return: None
        """
        print("Victory_Protocol Active")
        self.mqtt_client.send_message("player_lose", [])

    def user_quit(self):
        """
        Called when the user quits prior to the game's natural end. Makes the user lose and the robot shutdown
        :return: None
        """
        self.victory_protocol()
        self.robot.shutdown()
        self.shutdown()

    def loss_protocol(self):
        """
        Informs the user that they have won.
        :return: None
        """
        self.mqtt_client.send_message("player_win", [])

    def set_difficulty(self, difficulty):
        """
        Sets the game difficulty
        :param difficulty: a Str, either 'easy', 'medium', or 'hard'
        :return:
        """
        self.difficulty = difficulty
