"""
Developing a Tkinter window
"""

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com

class Window(object):

    def __init__(self, canvas):
        self.canvas = canvas

def main():

    root = tkinter.Tk()
    root.title("Rose Hulman Hallways")

    frame = ttk.Frame(root, padding=10)
    frame.grid()

    instructions = " Run away from teachers / To be determined "
    label = ttk.Label(frame, text=instructions)
    label.grid(columnspan=2)

    canvas = tkinter.Canvas(frame, background="lightgray", width=800, height=500)
    canvas.grid(columnspan=2)

    # Make callbacks for the two buttons.
    clear_button = ttk.Button(frame, text="Clear")
    clear_button.grid(row=3, column=0)
    clear_button["command"] = lambda: clear(canvas)

    quit_button = ttk.Button(frame, text="Quit")
    quit_button.grid(row=3, column=1)
    quit_button["command"] = lambda: quit_program(mqtt_client)

    # Create an MQTT connection
    my_delegate = Window(canvas)
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect("draw", "draw")

    root.mainloop()

def clear(canvas):
    """Clears the canvas contents"""
    canvas.delete("all")


def quit_program(mqtt_client):
    """For best practice you should close the connection.  Nothing really "bad" happens if you
       forget to close the connection though. Still it seems wise to close it then exit."""
    if mqtt_client:
        mqtt_client.close()
    exit()




main()