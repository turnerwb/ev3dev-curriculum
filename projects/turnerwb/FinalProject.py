# TODO 1: Verify that PIXY will work with LED, Note changes to camera needed to make it work
# TODO 2: Tkinter GUI, Red Light/Green Light Buttons, Call out button, Difficulty buttons?
# TODO 3: Random number generator to cause robot to 'Cheat.' Perhaps vary distance
# TODO 4: Robot/Light system
# DONE 5: Tkinter/Arduino System
# TODO 6: Test lag between Light change and robot stop. Is it slow enough that the user can see a delay if no cheat?
# TODO 8: MQTT Computer to Robot: Testing if the robot cheated
# (I'm thinking something like the Gamemaster from "Petals on a Rose")
# TODO 9: MQTT Robot to Computer: Testing how far the robot went (Decide on a victory condition)
import Tkinter_Window as GUI
import ArduinoController as arduino
import Communication as coms
import time


def main():
    startup_protocol()
    window = GUI.Window()
    window.green_button['command'] = lambda: green_protocol(window)
    window.red_button['command'] = lambda: red_protocol(window)
    window.cheat_button['command'] = lambda: accusation_protocol()
    window.root.bind('<space>', lambda event: spacebar_protocol(window))
    window.quit['command'] = lambda: shutdown_protocol(window)
    window.root.mainloop()


def startup_protocol():
    arduino.reset()


def green_protocol(window):
    window.green_button.state(['disabled'])
    window.red_button.state(['!disabled'])
    arduino.green_light()


def red_protocol(window):
    window.green_button.state(['!disabled'])
    window.red_button.state(['disabled'])
    arduino.red_light()


def spacebar_protocol(window):
    if window.red_button.instate(['!disabled']):
        red_protocol(window)
    else:
        green_protocol(window)


def accusation_protocol():
    coms.caught_cheating()


def shutdown_protocol(window):
    arduino.reset()
    time.sleep(.1)
    coms.shutdown()
    time.sleep(.1)
    window.shutdown()

main()
