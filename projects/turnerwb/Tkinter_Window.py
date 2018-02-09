import tkinter
from tkinter import ttk


# TODO 1 Add buttons for cheating
# TODO 2 Add difficulty buttons
# TODO 3 Make Window Look Nice
# TODO 4 New Game Window?
class Window(object):
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("Red Light, Green Light")

        self.frame = ttk.Frame(self.root, padding=200)
        self.frame.grid()

        ttk.Style().configure("C.TButton", background="green", foreground="green", padding=6)
        self.green_button = ttk.Button(self.frame, text="Green Light", style="C.TButton")

        ttk.Style().configure("TButton", background="red", foreground="red", padding=6)
        self.red_button = ttk.Button(self.frame, text="Red Light", style ="TButton")

        self.red_button.grid()
        self.green_button.grid()

    def display(self):
        self.root.mainloop()