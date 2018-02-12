# TODO 1: Verify that PIXY will work with LED, Note changes to camera needed to make it work
# DONE 2: Tkinter Gui, Red Light/Green Light Buttons, Call out button, Difficulty buttons?
# DONE 2A: Progress Bar on Tkinter? Other visual rep. of robot progress, Goes w/ TODO 9!!
# TODO 3: Random number generator to cause robot to 'Cheat.' Perhaps vary distance
# TODO 4: Robot/Light system
# DONE 5: Tkinter/Arduino System
# TODO 6: Test lag between Light change and robot stop. Is it slow enough that the user can see a delay if no cheat?
# TODO 7: MQTT Computer to Robot: Difficulty information
# TODO 8: MQTT Computer to Robot: Testing if the robot cheated
# (I'm thinking something like the Gamemaster from "Petals on a Rose")
# TODO 9: MQTT Robot to Computer: Testing how far the robot went (Decide on a victory condition)
# TODO 10: How to multitask and determine Win/Loss and Progress
# TODO 11: Add Doc Strings
import TkinterWindow as Gui
import ArduinoController as Arduino
import Communication as Coms
import time


def main():
    parameters = startup_protocol()
    if not parameters[0]:
        play_game(parameters[1].get())


def startup_protocol():
    Arduino.reset()
    newgame = Gui.NewGameWindow()
    newgame.quit['command'] = lambda: quit_early(newgame)
    newgame.proceed['command'] = lambda: init_game_protocol(newgame)
    newgame.root.mainloop()
    return newgame.game_parameters


def init_game_protocol(window):
    difficulty = window.difficulty
    window.root.destroy()
    window.difficulty = difficulty


def play_game(difficulty):
    print("You are playing in " + str(difficulty) + " mode!")
    window = Gui.Window()
    window.green_button['command'] = lambda: green_protocol(window)
    window.red_button['command'] = lambda: red_protocol(window)
    window.cheat_button['command'] = lambda: accusation_protocol()
    window.root.bind('<space>', lambda event: spacebar_protocol(window))
    window.quit['command'] = lambda: shutdown_protocol(window)
    window.root.mainloop()


def green_protocol(window):
    window.green_button.state(['disabled'])
    window.red_button.state(['!disabled'])
    Arduino.green_light()
    window.update_progress()


def red_protocol(window):
    window.green_button.state(['!disabled'])
    window.red_button.state(['disabled'])
    Arduino.red_light()


def spacebar_protocol(window):
    if window.red_button.instate(['!disabled']):
        red_protocol(window)
    else:
        green_protocol(window)


def accusation_protocol():
    Coms.caught_cheating()


def shutdown_protocol(window):
    Arduino.reset()
    time.sleep(.1)
    Coms.shutdown()
    time.sleep(.1)
    window.shutdown()


def quit_early(window):
    try:
        window.game_parameters[0] = True
        parameters = window.game_parameters
        window.shutdown()
        window.game_parameters = parameters
    except AttributeError:
        window.shutdown()


main()
