"""A simple spin the wheel game. There are three players and each one has
to try to get as close as possible to 100 points without going over."""

import tkinter as tk
import random

class Game(tk.Frame):
    """GUI application for the price is right."""

    wheel_numbers = ('100', '15', '50', '95', '20', '5', '45', '60', '35',
                     '90', '65', '40', '55', '75', '30', '85', '70', '25',
                     '80', '10')

    def __init__(self, parent):
        """Initialize GUI."""
        super().__init__(parent)
        self.parent = parent
        self.wheel_position = 0

        self.create_widgets()

    def create_widgets(self):
        """Create widgets."""
        self.play_button = tk.Button(self.parent, text='Roda!', 
                                     command=self.on_play_button, 
                                     height=38, width=10)
        self.play_button.grid(row=0, column=0, sticky='W')

        img = tk.PhotoImage(file="imgs/wheel_5.png")
        self.photo_lbl = tk.Label(self.parent, image=img, text='',
                                  borderwidth=0)
        self.photo_lbl.grid(row=0, column=1, columnspan=10, sticky='W')
        self.photo_lbl.image = img
        self.photo_lbl.bind('<Button-1>', self.mouse_bt_pressed)
        self.photo_lbl.bind('<ButtonRelease-1>', self.mouse_bt_released)

    def on_play_button(self):
        """Action of spinning the wheel using a button."""
        print("Spin!")

    def mouse_bt_pressed(self, event):
        """Callback function for clicking button on the wheel."""
        print("SSpinnig!", event.x, event.y)
    
    def mouse_bt_released(self, event):
        """Callback function for release button on wheel."""
        print("Spin that wheel!!!", event.x, event.y)
        self.spin_wheel()

    def update_image(self):
        """Update wheel image."""
        file_name = f"imgs/wheel_{self.wheel_numbers[self.wheel_position]}.png"
        img = tk.PhotoImage(file=file_name)
        self.photo_lbl.config(image=img)
        self.photo_lbl.image = img
        if self.wheel_position < (len(self.wheel_numbers) - 1):
            self.wheel_position += 1
        else:
            self.wheel_position = 0

    def spin_wheel(self):
        """Make wheel spin."""
        self.parent.after(100, self.update_image)


def main():
    """Start here."""
    root = tk.Tk()
    root.title("The Price is Right")
    root.geometry('1200x800')
    game = Game(root)
    root.mainloop()

if __name__ == '__main__':
    main()