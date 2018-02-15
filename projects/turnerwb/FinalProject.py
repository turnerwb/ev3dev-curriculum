"""
FinalProject.py:
Serves as the main function for the Red Light/Green Light game on the PC end. Handles combining TkinterWindow.py,
ArduinoController.py, and Communication.py to allow communication between the computer and the Arduino and the computer
and the Robot.
Author: Wesley B. Turner
"""

import TkinterWindow as Gui
import ArduinoController as Arduino
import Communication as Coms
import time
# Global variable RUNNING tells when game has been exited by user
RUNNING = True


def main():
    global RUNNING
    while RUNNING:  # While the user hasn't quit, continue to run the game
        parameters = startup_protocol()
        if not parameters[0]:
            play_game(parameters[1].get())


def startup_protocol():
    Arduino.reset()  # Turn off lights
    newgame = Gui.NewGameWindow()
    newgame.quit['command'] = lambda: quit_early(newgame)
    newgame.proceed['command'] = lambda: init_game_protocol(newgame)
    newgame.root.mainloop()  # Run NewGameWindow and allow the user to either quit or select a difficulty
    return newgame.game_parameters  # Returns the game parameters


def init_game_protocol(window):
    """
    Starts a new game from the NewGameWindow, destroying that window
    :param window: a NewGameWindow
    :return: None
    """
    difficulty = window.difficulty
    window.root.destroy()
    window.difficulty = difficulty


def play_game(difficulty):
    """
    Main window to play the game, allows the user to control the Arduino
    :param difficulty: a Str, either 'easy', 'medium', or 'hard'
    :return: None
    """
    print("You are playing in " + str(difficulty) + " mode!")
    window = Gui.Window()
    com = Coms.CommunicationSystem(window)
    com.set_difficulty(str(difficulty))
    window.green_button['command'] = lambda: green_protocol(window)
    window.red_button['command'] = lambda: red_protocol(window)
    window.cheat_button['command'] = lambda: accusation_protocol(com)
    window.root.bind('<space>', lambda event: spacebar_protocol(window))
    window.quit['command'] = lambda: shutdown_protocol(window, com, True)
    window.root.bind('<a>', lambda event: com.player_win())
    window.root.bind('<s>', lambda event: com.player_lose())
    if window.root.state == 'normal':
        window.update_progress()
    window.root.mainloop()
    if window.done:
        end_game(window.victory)


def green_protocol(window):
    """
    Turns on the green light and disables the button, enabling the red button
    :param window: a Window
    :return:
    """
    window.green_button.state(['disabled'])
    window.red_button.state(['!disabled'])
    Arduino.green_light()


def red_protocol(window):
    """
    Turns on the Red LED and disables the button, enabling the Green Button
    :param window: a Window
    :return: None
    """
    window.green_button.state(['!disabled'])
    window.red_button.state(['disabled'])
    Arduino.red_light()


def spacebar_protocol(window):
    """
    Allows the user to toggle buttons with the spacebar
    :param window: a Window
    :return: None
    """
    if window.red_button.instate(['!disabled']):
        red_protocol(window)
    else:
        green_protocol(window)


def accusation_protocol(com):
    """
    Allows the user to accuse the robot of cheating
    :param com: a CommunicationSystem
    :return: None
    """
    com.caught_cheating()


def shutdown_protocol(window, com, early_exit=False):
    """
    Ends the game and calls functions to reset the other objects
    :param window: a Window
    :param com: a CommunicationSystem
    :param early_exit: a Boolean, tells if the user quit before the game ended naturally
    :return: None
    """
    Arduino.reset()
    time.sleep(.1)
    com.shutdown(early_exit)
    time.sleep(.1)
    window.shutdown()


def quit_early(window):
    """
    Allows user to quit from NewGameWindow
    :param window: a NewGameWindow
    :return: None
    """
    try:
        window.game_parameters[0] = True
        parameters = window.game_parameters
        window.shutdown()
        window.game_parameters = parameters
    except AttributeError:
        window.shutdown()
    global RUNNING
    RUNNING = False


def end_game(victory):
    """
    Shows a GameOverWindow for the user and resets the lights
    :param victory: a Boolean, True if the user won, False if they lost
    :return: None
    """
    print("ENDING GAME")
    Arduino.reset()
    window = Gui.GameOverWindow(victory)
    window.quit['command'] = lambda: close_app(window)
    window.proceed['command'] = lambda: window.root.destroy()
    window.root.mainloop()


def close_app(window):
    """
    Allows the user to quit from GameOverWindow
    :param window: a GameOverWindow
    :return: None
    """
    global RUNNING
    RUNNING = False
    window.root.destroy()


main()
