import mqtt_remote_method_calls as Com


class CommunicationSystem(object):
    # TODO Write victory/defeat functions
    def __init__(self, window):
        self.mqtt_client = Com.MqttClient(self)
        self.window = window
        self.mqtt_client.connect_to_ev3()

    def caught_cheating(self):
        print("J'Accuse!")

    def update_progress(self, update_amount):
        self.window.track += update_amount
        self.window.update_progress()

    def shutdown(self):
        print("Shutting down Coms")
        self.mqtt_client.close()

    def player_win(self):
        self.window.game_over(True)
        self.shutdown()

    def player_lose(self):
        self.window.game_over(False)
        self.shutdown()

