"""A simple spin the wheel game. There are three players and each one has
to try to get as close as possible to 100 points without going over."""

import tkinter as tk
import random

class Game(tk.Frame):
    """GUI application for the price is right."""

    def __init__(self, parent):
        """Initialize GUI."""
        super().__init__(parent)
        self.parent = parent

        self.create_widgets()

    def create_widgets(self):
        """Create widgets."""
        self.play_button = tk.Button(self.parent, text='Roda!', 
                                     command=self.spin_wheel, 
                                     height=38, width=10)
        self.play_button.grid(row=0, column=0, sticky='W')

        img = tk.PhotoImage(file="imgs/wheel_5.png")
        self.photo_lbl = tk.Label(self.parent, image=img, text='',
                                  borderwidth=0)
        self.photo_lbl.grid(row=0, column=1, columnspan=10, sticky='W')
        self.photo_lbl.image = img
        self.photo_lbl.bind('<B1-Motion>', self.push_the_wheel)

    def spin_wheel(self):
        """Action of spinning the wheel using a button."""
        print("Spin!")

    def push_the_wheel(self, event):
        """Spin the wheel using a motion event."""
        print("Spin!", event.x, event.y)


def main():
    """Start here."""
    root = tk.Tk()
    root.title("The Price is Right")
    root.geometry('1200x800')
    game = Game(root)
    root.mainloop()

if __name__ == '__main__':
    main()