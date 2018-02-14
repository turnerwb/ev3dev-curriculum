import mqtt_remote_method_calls as Com


class EV3CommunicationSystem(object):

    def __init__(self):
        self.mqtt_client = Com.MqttClient(self)
        self.mqtt_client.connect_to_pc()
        self.cheated = False
        self.caught = False
        self.difficulty = None

    def update_progress(self, update_amount, cheated):
        self.mqtt_client.send_message("update_progress", [update_amount])
        self.cheated = cheated

    def shutdown(self):
        print("Shutting down Coms")
        self.mqtt_client.close()

    def accused_cheating(self):
        if self.cheated:
            self.caught = True
        else:
            self.mqtt_client.send_message("wrong_guess", [])

    def victory_protocol(self):
        self.mqtt_client.send_message("player_lose", [])

    def loss_protocol(self):
        self.mqtt_client.send_message("player_win", [])

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
