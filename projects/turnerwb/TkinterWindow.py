"""
TkinterWindow.py
Creates the various Tkinter windows for the FinalProject:
Window: Main game window
NewGameWindow: Window for user to define difficulty
GameOverWindow: Window that informs user if they have won or lost and allows them to quit or start a new game
"""
import tkinter
from tkinter import ttk

class Window(object):
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("Red Light, Green Light")

        self.frame = ttk.Frame(self.root, padding=10)
        self.frame.grid()

        ttk.Style().configure("A.TButton", background="green", foreground="green", padding=6)
        self.green_button = ttk.Button(self.frame, text="Green Light", style="A.TButton")

        ttk.Style().configure("B.TButton", background="red", foreground="red", padding=6)
        self.red_button = ttk.Button(self.frame, text="Red Light", style="B.TButton")

        ttk.Style().configure("C.TButton", background="slate gray", foreground="slate gray", padding=6)
        self.cheat_button = ttk.Button(self.frame, text="The Robot Didn't Stop!", style="C.TButton")

        self.quit = ttk.Button(self.frame, text="Quit")

        self.track = 0
        self.progress = ttk.Progressbar(self.frame, orient="horizontal", length=200, value=self.track,
                                        mode='determinate', maximum=1000)

        self.progress.grid(row=6, column=1)
        self.green_button.grid(row=3, column=1)
        self.red_button.grid(row=1, column=1)
        self.cheat_button.grid(row=5, column=1)
        self.quit.grid(row=7, column=5)

        self.victory = None
        self.done = False

    def shutdown(self):
        self.root.destroy()

    def update_progress(self):
        try:
            self.progress.configure(value=self.track)
            self.root.after(1000, self.update_progress)
        except tkinter.TclError:
            pass

    def game_over(self, victory):
        self.done = True
        self.victory = victory


class NewGameWindow(object):
    def __init__(self):
        self.end = False

        self.root = tkinter.Tk()
        self.root.title("Red Light, Green Light")

        self.frame = ttk.Frame(self.root, padding=10)
        self.frame.grid()

        self.difficulty = tkinter.StringVar(value='easy')
        self.easy = ttk.Radiobutton(self.frame, text='Easy', variable=self.difficulty, value='easy')
        self.medium = ttk.Radiobutton(self.frame, text='Medium', variable=self.difficulty, value='medium')
        self.hard = ttk.Radiobutton(self.frame, text='Hard', variable=self.difficulty, value='hard')

        self.label = ttk.Label(self.frame, text="Select A Difficulty, Defaults to Easy")

        self.proceed = ttk.Button(self.frame, text="New Game")
        self.quit = ttk.Button(self.frame, text="Quit")

        self.label.grid(row=0, column=1)

        self.easy.grid(row=1, column=0)
        self.easy.selection_own()
        self.medium.grid(row=1, column=1)
        self.hard.grid(row=1, column=2)

        self.quit.grid(row=3, column=2)
        self.proceed.grid(row=3, column=0)

        self.game_parameters = [self.end, self.difficulty]

    def shutdown(self):
        self.root.destroy()
        self.end = True


class GameOverWindow(object):

    def __init__(self, victory):
        self.root = tkinter.Tk()
        self.root.title("Game Over")

        self.frame = ttk.Frame(self.root, padding=10)
        self.frame.grid()

        self.text = ttk.Label(self.frame, text="Game Over!")
        self.text.grid(row=0, column=1)

        if victory:
            self.victory_text = ttk.Label(self.frame, text="You Win!")
        else:
            self.victory_text = ttk.Label(self.frame, text="You Lost!")
        self.victory_text.grid(row=1, column=1)

        self.proceed = ttk.Button(self.frame, text="New Game")
        self.quit = ttk.Button(self.frame, text="Quit")

        self.proceed.grid(row=2, column=0)
        self.quit.grid(row=2, column=2)

    def shutdown(self):
        self.root.destroy()
