"""
Creates the various Tkinter windows for the FinalProject:
Window: Main game window
"""
import tkinter
from tkinter import ttk

# DONE 1 Add buttons for cheating
# DONE 2 Add difficulty buttons
# TODO 3 Make Window Look Nice
# TODO 4 New Game Window?
# TODO 5 Progress Bar for distance until victory
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

        self.difficulty = None
        self.easy = ttk.Radiobutton(self.frame, text='Easy', variable=self.difficulty, value='easy')
        self.medium = ttk.Radiobutton(self.frame, text='Medium', variable=self.difficulty, value='medium')
        self.hard = ttk.Radiobutton(self.frame, text='Hard', variable=self.difficulty, value='hard')

        self.progress.grid(row=6, column=1)
        self.green_button.grid(row=3, column=1)
        self.red_button.grid(row=1, column=1)
        self.cheat_button.grid(row=5, column=1)
        self.quit.grid(row=7, column=5)

    def display(self):
        self.root.mainloop()

    def shutdown(self):
        self.root.destroy()
