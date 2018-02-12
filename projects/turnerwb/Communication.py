import mqtt_remote_method_calls as Com


class CommunicationSystem(object):

    def __init__(self, window):
        self.mqtt_client = Com.MqttClient(self)
        self.window = window
        self.mqtt_client.connect_to_ev3()

    def caught_cheating(self):
        print("J'Accuse!")
        self.window.shutdown()

    def update_progress(self, update_amount):
        self.window.track += update_amount
        self.window.update_progress()

    def shutdown(self):
        print("Shutting down Coms")