"""A simple spin the wheel game. There are three players and each one has
to try to get as close as possible to 100 points without going over."""

import tkinter as tk
import time
import math



class Game(tk.Frame):
    """GUI application for the price is right."""

    WHEEL_SPIN_MULTIPLIER = 50_000
    WHEEL_STOP_STEP = 500
    WHEEL_DAMPENING = 1.05
    WHEEL_NUMBERS = ('100', '15', '50', '95', '20', '5', '45', '60', '35',
                     '90', '65', '40', '55', '75', '30', '85', '70', '25',
                     '80', '10')
    INSTRUCTIONS = ('Instructions:\n\n'
                    'There are three players. Wins who gets closer to 100'
                    ' without going over. Each player starts by spinning the'
                    ' wheel once. After that, she can choose to spin it a'
                    ' second time or not. Anyone who goes over 100 looses'
                    ' immediately. In the end the player closer to 100 that'
                    ' did not go over, wins!\n\n'
                    'Statistics are presented to display who has the better'
                    ' chance of whinning.')

    def __init__(self, parent):
        """Initialize GUI."""
        super().__init__(parent)
        self.parent = parent
        self.wheel_position = 0

        self.create_widgets()
        self.create_wheel_imgs()

    def create_widgets(self):
        """Create widgets."""
        defaultbg = self.parent.cget('bg')
        self.title_txt = tk.Label(self.parent, text='The Price is Right!',
                                  anchor=tk.CENTER, bg=defaultbg,
                                  font=('Arial', '32', 'bold'), fg='dark grey',
                                  height=2, width=20)
        self.title_txt.grid(row=0, column=0, columnspan=10, sticky='N')

        img = tk.PhotoImage(file="imgs/wheel_100.png")
        self.photo_lbl = tk.Label(self.parent, image=img, text='',
                                  borderwidth=0)
        self.photo_lbl.grid(row=1, column=0, columnspan=10, sticky='W')
        self.photo_lbl.image = img
        self.photo_lbl.bind('<Button-1>', self.mouse_bt_pressed)
        self.photo_lbl.bind('<ButtonRelease-1>', self.mouse_bt_released)

        self.instr_frame = tk.Frame(self.parent, height=50, width=50)
        self.instr_frame.grid(row=1, column=11, columnspan=1, sticky='N', ipadx=0)

        self.create_instr_frame_widgets()

        self.result_txt = tk.Label(self.parent, text='0')
        self.result_txt.grid(row=2, column=0, columnspan=1, sticky='N')

        
    def create_instr_frame_widgets(self):
        """Create widgets inside instructions frame, to the right of the 
        photo."""

        self.instruction_txt = tk.Label(self.instr_frame, text=self.INSTRUCTIONS, 
                                        height=15, width=50, justify=tk.LEFT, 
                                        font=('Arial', '10'), anchor='n', 
                                        wraplength=370, borderwidth=1, relief='solid')
        self.instruction_txt.grid(row=0, column=0, columnspan=5)

        score_board_input = [
            ('1st spin', 6, 1, 1), ('2nd spin', 6, 1, 2), ('total', 6, 1, 3),
            ('1st player', 10, 2, 0), ('2nd player', 10, 3, 0), 
            ('3rd player', 10, 4, 0)
            ]
        for text, width, row, column in score_board_input:
            self.lbl = tk.Label(self.instr_frame, text=text, height=1, 
                                width=width, font=('Arial', '10'), anchor='n', 
                                borderwidth=1, relief='solid')
            self.lbl.grid(row=row, column=column, sticky='w')

        self.score_txt_list = []
        for r in range(3):
            scores_row = []
            for c in range(3):
                txt = tk.Text(self.instr_frame, height=1, width=5)
                txt.grid(row=r + 2, column=c + 1, sticky='w')
                scores_row.append(txt)
            self.score_txt_list.append(scores_row)


    def create_wheel_imgs(self):
        """Load wheel images into tuple."""
        wheel_imgs_list = []
        for wheel_number in self.WHEEL_NUMBERS:
            file_name = f"imgs/wheel_{wheel_number}.png"
            img = tk.PhotoImage(file=file_name)
            wheel_imgs_list.append(img)
        self.wheel_imgs = tuple(wheel_imgs_list)

    def mouse_bt_pressed(self, event):
        """Callback function for clicking button on the wheel."""
        self.wheel_init_time = time.time()
        print("SSpinnig!", event.x, event.y)
        self.wheel_init_y = event.y
    
    def mouse_bt_released(self, event):
        """Callback function for release button on wheel."""
        self.wheel_dif_time = time.time() - self.wheel_init_time
        print("Spin that wheel!!!", event.x, event.y)
        self.wheel_dif_y = event.y - self.wheel_init_y
        if self.wheel_dif_y > 0.1:
            self.calculate_init_wheel_step()
            self.push_wheel()

    def spin_wheel(self):
        """Make wheel spin using sequence of images."""
        self.photo_lbl.config(image=self.wheel_imgs[self.wheel_position])
        self.photo_lbl.image = self.wheel_imgs[self.wheel_position]        
        self.push_wheel()

    def calculate_init_wheel_step(self):
        """Calculate initial step for spinning wheel as a function of time 
        difference between mouse button pressed and released and y positions
        of mouse."""
        self.wheel_spin_factor = self.wheel_dif_time / self.wheel_dif_y
        self.step = math.ceil(self.wheel_spin_factor 
                              * self.WHEEL_SPIN_MULTIPLIER)
        

    def push_wheel(self):
        """Control movement of wheel."""
        self.step = math.ceil(self.step * self.WHEEL_DAMPENING)
        print(self.step)
        if self.step < self.WHEEL_STOP_STEP:
            self.parent.after(self.step, self.spin_wheel)
            if self.wheel_position < (len(self.WHEEL_NUMBERS) - 1):
                self.wheel_position += 1
            else:
                self.wheel_position = 0
        else:
            self.result_txt.config(text=self
                                   .WHEEL_NUMBERS[self.wheel_position])



def main():
    """Start here."""
    root = tk.Tk()
    root.title("The Price is Right")
    root.geometry('1200x760')
    game = Game(root)
    root.mainloop()

if __name__ == '__main__':
    main()