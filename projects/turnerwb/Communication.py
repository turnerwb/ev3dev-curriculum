import mqtt_remote_method_calls as Com


class CommunicationSystem(object):
    # DONE Write victory/defeat functions
    # TODO Write comm for robot in case of early quit from game window
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
        self.window.root.destroy()

    def player_lose(self):
        self.window.game_over(False)
        self.shutdown()
        self.window.root.destroy()

    def set_difficulty(self, difficulty):
        self.mqtt_client.send_message("set_difficulty", [difficulty])
