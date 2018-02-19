""" Message client for the game of Rose Hulman """

import tkinter
from tkinter import ttk


import mqtt_remote_method_calls as com

# Potential values of the color_sensor.color property
#   ev3.ColorSensor.COLOR_NOCOLOR is the value 0
#   ev3.ColorSensor.COLOR_BLACK   is the value 1
#   ev3.ColorSensor.COLOR_BLUE    is the value 2
#   ev3.ColorSensor.COLOR_GREEN   is the value 3
#   ev3.ColorSensor.COLOR_YELLOW  is the value 4
#   ev3.ColorSensor.COLOR_RED     is the value 5
#   ev3.ColorSensor.COLOR_WHITE   is the value 6
#   ev3.ColorSensor.COLOR_BROWN   is the value 7


class Colors(object):

    def __init__(self):

        self.blue = 1
        self.white = 2
        self.green = 3
        self.red = 4


class MyDelegate(object):

    def __init__(self, label_to_display_messages):
        self.display_label = label_to_display_messages

    def score_change_display(self, score):

        message_to_display = "Score {}".format(score)
        self.display_label.configure(text=message_to_display)

    def end_of_game(self, score):

        if score > 99:
            message_to_display = "YOU HAVE WON THE GAME!"
            self.display_label.configure(text=message_to_display)


def main():

    colors = Colors()
    root = tkinter.Tk()
    root.title("--Game of Rose Hulman--")

    main_frame = ttk.Frame(root, padding=55, relief='raised')
    main_frame.grid()

    head_label = ttk.Label(main_frame, text="Beware of 'Hard' Teachers...")
    head_label.grid(row=0, column=1)

    yellow_button = ttk.Button(main_frame, text="Yellow -> Good Test")
    yellow_button.grid(row=2, column=0)
    yellow_button['command'] = lambda: send_color_command(mqtt_client, 4)

    white_button = ttk.Button(main_frame, text="White -> Cheap Housing")
    white_button.grid(row=3, column=0)
    white_button['command'] = lambda: send_color_command(mqtt_client, 6)

    blue_button = ttk.Button(main_frame, text="Black -> Good Food")
    blue_button.grid(row=2, column=2)
    blue_button['command'] = lambda: send_color_command(mqtt_client, colors.blue)

    green_button = ttk.Button(main_frame, text="Green -> Good Job")
    green_button.grid(row=3, column=2)
    green_button['command'] = lambda: send_color_command(mqtt_client, colors.green)

    quit_button = ttk.Button(main_frame, text="Quit")
    quit_button.grid(row=5, column=2)
    quit_button['command'] = lambda: quit_command(mqtt_client)

    message_ev3 = ttk.Label(main_frame, text="Score: 0")
    message_ev3.grid(row=3, column=1)

    gap = ttk.Label(main_frame, text="")
    gap.grid(row=4, column=2)

    pcDelegate = MyDelegate(message_ev3)
    mqtt_client = com.MqttClient(pcDelegate)
    pcDelegate.mqtt_client = mqtt_client
    mqtt_client.connect_to_ev3("broker.mqttdashboard.com")

    root.mainloop()


def send_color_command(mqtt_client, color):

    print("Input = {}".format(color))
    mqtt_client.send_message("input_seek", [color])


def quit_command(mqtt_client):

    print("Sending quit command")
    mqtt_client.send_message("shutdown")


main()