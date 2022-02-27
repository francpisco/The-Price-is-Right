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


def main():
    """Start here."""
    root = tk.Tk()
    root.title("The Price is Right")
    root.geometry('1280x820')
    game = Game(root)
    root.mainloop()

if __name__ == '__main__':
    main()