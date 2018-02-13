import mqtt_remote_method_calls as Com


class EV3CommunicationSystem(object):

    def __init__(self):
        self.mqtt_client = Com.MqttClient(self)
        self.mqtt_client.connect_to_pc()
        self.cheated = False

    def update_progress(self, update_amount, cheated):
        self.mqtt_client.send_message("update_progress", [update_amount])
        self.cheated = cheated

    def shutdown(self):
        print("Shutting down Coms")

    def accused_cheating(self):
        pass
        # if self.cheated: