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
        self.play_button = tk.Button(self.parent, text='Spin!', 
                                     command=self.spin_wheel)
        self.play_button.grid(row=0, column=0, sticky='W')

        img = tk.PhotoImage(file="imgs/wheel_5.png")
        self.photo_lbl = tk.Label(self.parent, image=img, text='',
                                  borderwidth=0)
        self.photo_lbl.grid(row=0, column=1, columnspan=10, sticky='W')
        self.photo_lbl.image = img

    def spin_wheel(self):
        """Action of spinning the wheel."""
        print("Spin!")


def main():
    """Start here."""
    root = tk.Tk()
    root.title("The Price is Right")
    root.geometry('1200x880')
    game = Game(root)
    root.mainloop()

if __name__ == '__main__':
    main()