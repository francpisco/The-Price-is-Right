"""A simple spin the wheel game. There are three players and each one has
to try to get as close as possible to 100 points without going over."""

import tkinter as tk
import time
import math
import sys



class Game(tk.Frame):
    """GUI application for the price is right."""

    WHEEL_SPIN_MULTIPLIER = 50_000
    WHEEL_STOP_STEP = 500
    WHEEL_DAMPENING = 1.1  # Must be about 1.1
    WHEEL_NUMBERS = ('100', '15', '50', '95', '20', '5', '45', '60', '35',
                     '90', '65', '40', '55', '75', '30', '85', '70', '25',
                     '80', '10')
    INSTRUCTIONS = ('Instructions:\n\n'
                    'The game consists of three players trying to get to as'
                    ' close to 100 points as possible by spinning the wheel.'
                    ' After the first spin, each player choses if she wants to'
                    ' spin the wheel a second time. Anyone that goes above'
                    ' 100 points looses.\n'
                    'The wheel must make at least a full rotation for the' 
                    ' play to be valid.\n'
                    'Wheel speed is a function of sweeping speed and'
                    ' distance.\n'
                    'Whoever gets closer to 100 without going'
                    ' above, wins!\n\n'
                    'Swipe on wheel with touchscreen or mouse to spin wheel.')
    ROTATION_WARNING = ('Wheel did not make a full rotation. Please repeat'
                        ' play!')

    def __init__(self, parent):
        """Initialize GUI."""
        super().__init__(parent)
        self.parent = parent
        self.start()
        self.create_widgets()
        self.create_wheel_imgs()
        
    def start(self):
        """Start a game."""
        self.game_finished = False
        self.wheel_position = 0
        self.current_player = 0  # 0 - 1st player, 1 - 2nd, 2 - 3rd 
        self.current_spin = 0  # 0 - 1sr, 1 - 2nd
        self.player_scores = [0, 0, 0]
        self.wheel_active = False
        self.show_player_total = False
        self.introduction_box()

    def create_widgets(self):
        """Create widgets."""
        defaultbg = self.parent.cget('bg')
        self.title_lbl = tk.Label(self.parent, text='The Price is Right!',
                                  anchor=tk.CENTER, bg=defaultbg,
                                  font=('Tahoma', '40', 'bold', 'italic'), 
                                  fg='blue', height=2, width=20)
        self.title_lbl.grid(row=0, column=0, columnspan=3, sticky='N')

        arrow_img = tk.PhotoImage(file="imgs/arrow.png")
        self.arrow_lbl = tk.Label(self.parent, image=arrow_img, text='',
                                  borderwidth=0)
        self.arrow_lbl.grid(row=1, column=0, columnspan=1, sticky='W')
        self.arrow_lbl.image = arrow_img

        img = tk.PhotoImage(file="imgs/wheel_100.png")
        self.photo_lbl = tk.Label(self.parent, image=img, text='',
                                  borderwidth=1, relief='solid')
        self.photo_lbl.grid(row=1, column=1, columnspan=1, sticky='W')
        self.photo_lbl.image = img
        self.photo_lbl.bind('<Button-1>', self.mouse_bt_pressed)
        self.photo_lbl.bind('<ButtonRelease-1>', self.mouse_bt_released)

        self.instr_frame = tk.Frame(self.parent, height=50, width=50)
        self.instr_frame.grid(row=1, column=2, columnspan=1, sticky='N', ipadx=0)

        self.create_right_frame_widgets()

    def introduction_box(self):
        """Create an introduction pop up box to display instructions and
        introduce game."""
        self.intro_box = tk.Toplevel()
        self.intro_box.wm_title('Introduction')
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        self.intro_box.geometry(f'520x360+{parent_x + 200}+{parent_y + 200}')

        inst_lbl = tk.Label(self.intro_box, text=self.INSTRUCTIONS, height=12, 
                            width=55, justify=tk.LEFT, font=('Tahoma', '12'),
                            anchor='n', wraplength=450, borderwidth=0,
                            pady=20)
        inst_lbl.grid(row=0, column=0, columnspan=5)

        play_btn = tk.Button(self.intro_box, text='Play', width=15, 
                             font=('Tahoma', '12', 'bold'), pady=5,
                             command=self.start_game)
        play_btn.grid(row=1, column=2)
        self.intro_box.attributes('-topmost', 'true')
        self.intro_box.protocol('WM_DELETE_WINDOW', self.start_game)

    def start_game(self):
        """Close introduction box and start game."""
        self.parent.attributes('-topmost', 'true')
        self.intro_box.destroy()
        self.wheel_active = True
        self.game_play_txt.delete('1.0', 'end')
        self.game_play_txt.insert('1.0', '1st Player, spin the wheel!')
        self.parent.attributes('-topmost', 'false')

        
    def create_right_frame_widgets(self):
        """Create widgets inside frame on the right to the photo."""

        defaultbg = self.instr_frame.cget('bg')
        self.game_play_txt = tk.Text(self.instr_frame, width=23, height=1, 
                                     bg=defaultbg, borderwidth=0, 
                                     font=('Tahoma', '18', 'bold'), fg='green')
        self.game_play_txt.grid(row=0, column=0, columnspan=4, padx=20, 
                                pady=50)

        score_board_input = [
            ('1st spin', 1, 1), ('2nd spin', 1, 2), ('total', 1, 3),
            ('1st player', 2, 0), ('2nd player', 3, 0), 
            ('3rd player', 4, 0)
            ]
        for text, row, column in score_board_input:
            self.lbl = tk.Label(self.instr_frame, text=text, height=2, 
                                width=10, font=('Tahoma', '12'), anchor='n', 
                                borderwidth=0)
            self.lbl.grid(row=row, column=column, sticky='n', pady=10, padx=0)

        self.score_txt_list = []
        for r in range(3):
            scores_row = []
            for c in range(3):
                txt = tk.Text(self.instr_frame, height=1, width=3, font=('Tahoma', '12'))
                txt.grid(row=r + 2, column=c + 1, sticky='n', pady=10)
                scores_row.append(txt)
            self.score_txt_list.append(scores_row)

    def play_again(self):
        """Actions to take to start over."""
        self.popup_gameover.destroy()
        self.start()
        self.update_wheel_img()
        self.reset_scores()

    def reset_scores(self):
        """Delete board scores from previous game."""
        for r in range(3):
            for c in range(3):
                self.score_txt_list[r][c].delete('1.0', 'end')


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
        self.wheel_init_y = event.y
    
    def mouse_bt_released(self, event):
        """Callback function for release button on wheel."""
        if self.wheel_init_y == event.y:
            return
        self.wheel_dif_time = time.time() - self.wheel_init_time
        self.wheel_dif_y = event.y - self.wheel_init_y
        self.calculate_init_wheel_step()
        if self.step < self.WHEEL_STOP_STEP and self.wheel_active:
            self.initial_wheel_pos = self.wheel_position
            self.complete_Wheel_turn = False
            self.spin_wheel()

    def update_wheel_img(self):
        """Make wheel spin using sequence of images."""
        self.photo_lbl.config(image=self.wheel_imgs[self.wheel_position])
        self.photo_lbl.image = self.wheel_imgs[self.wheel_position]         

    def calculate_init_wheel_step(self):
        """Calculate initial step for spinning wheel as a function of time 
        difference between mouse button pressed and released and y positions
        of mouse."""
        self.wheel_spin_factor = self.wheel_dif_time / self.wheel_dif_y
        self.step = math.ceil(self.wheel_spin_factor 
                              * self.WHEEL_SPIN_MULTIPLIER)
        
    def spin_wheel(self):
        """Control movement of wheel.""" 
        print(self.step)
        if self.step < self.WHEEL_STOP_STEP:
            if self.wheel_position < (len(self.WHEEL_NUMBERS) - 1):
                self.wheel_position += 1
            else:
                self.wheel_position = 0
            self.update_wheel_img()
            self.parent.after(self.step, self.calculate_next_step)
            if self.wheel_position == (self.initial_wheel_pos):
                self.complete_Wheel_turn = True
        else:
            if self.complete_Wheel_turn is False:
                self.popup_wheel_turn()
            else:
                self.proceed_game()

    def calculate_next_step(self):
        """Determine next step for wheel movement and call 
        spin_wheel() again."""
        self.step = math.ceil(self.step * self.WHEEL_DAMPENING)       
        self.spin_wheel()


    def popup_wheel_turn(self):
        """Display a popup warning that the wheel did not make a full 
        rotation."""
        self.turn_popup = tk.Toplevel()
        self.turn_popup.wm_title('Must Make a Complete Rotation')
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        self.turn_popup.geometry(f'520x360+{parent_x + 200}+{parent_y + 200}')

        info_lbl = tk.Label(self.turn_popup, text=self.ROTATION_WARNING, 
                            height=1, width=52, justify=tk.LEFT, 
                            font=('Tahoma', '12', 'bold'), fg='red',
                            anchor='n', borderwidth=0, pady=70)
        info_lbl.grid(row=0, column=0, columnspan=1)

        btn_txt = "Repeat"
        play_btn = tk.Button(self.turn_popup, text=btn_txt, 
                             font=('Tahoma', '12', 'bold'),
                             command=self.repeat_play, pady=5, padx=30)
        play_btn.grid(row=1, column=0)
        self.wheel_active = False
        self.turn_popup.protocol('WM_DELETE_WINDOW', self.repeat_play)

    def repeat_play(self):
        """Called when wheel doesn't make a full turn. must reset wheel to 
        where it was before this spin."""
        self.wheel_position = self.initial_wheel_pos
        self.update_wheel_img()
        self.turn_popup.destroy()
        self.wheel_active = True

    def proceed_game(self):
        """Control flow of game after 1st spin. What happens after wheel 
        stops"""
        self.display_players_scores()      
        if self.current_spin == 0:
            self.ask_2nd_spin()
        elif self.current_player < 2:
            self.display_total()
            self.show_player_total = True
            self.display_game_popup()
            self.update_game_txt()
            self.current_spin = 0
            self.current_player += 1
        else:
            self.display_total()
            self.update_game_txt()
            self.end_game()

    def display_game_popup(self):
        """Display a popup at the end of each player's turn."""
        self.game_popup = tk.Toplevel()
        self.game_popup.wm_title('Player total')
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        self.game_popup.geometry(f'520x360+{parent_x + 200}+{parent_y + 200}')

        info_txt = (f'Player {self.current_player + 1} total:'
                    f' {self.player_scores[self.current_player]}')
        info_lbl = tk.Label(self.game_popup, text=info_txt, height=1, 
                            width=42, justify=tk.LEFT, font=('Tahoma', '16'),
                            anchor='n', borderwidth=0, pady=80)
        info_lbl.grid(row=0, column=0, columnspan=1)

        if self.current_player < 2:
            btn_txt = f'Player {self.current_player + 2}, play!'
        else:
            btn_txt = 'Continue'
        play_btn = tk.Button(self.game_popup, text=btn_txt, 
                             font=('Tahoma', '12', 'bold'), pady=5, padx=30, 
                             command=self.continue_game)
        play_btn.grid(row=1, column=0)
        self.wheel_active = False
        self.game_popup.protocol('WM_DELETE_WINDOW', self.continue_game)

    def continue_game(self):
        """Close game pop up window and continue game."""
        self.game_popup.destroy()
        self.show_player_total = False
        if not self.game_finished:
            self.wheel_active = True
            self.update_game_txt()
        

    def display_players_scores(self):
        """Display players scores on scoreboard as wheel stops."""
        self.player_scores[self.current_player] += (
            int(self.WHEEL_NUMBERS[self.wheel_position]))
        self.score_txt_list[self.current_player][self.current_spin] \
            .delete('1.0', 'end')
        self.score_txt_list[self.current_player][self.current_spin] \
            .insert('1.0', self.WHEEL_NUMBERS[self.wheel_position])

    def display_total(self):
        """Display total at the end of a player's turn."""
        player_total = self.player_scores[self.current_player]
        self.score_txt_list[self.current_player][2].insert('1.0', player_total)

    def ask_2nd_spin(self):
        """Ask player if she wants to spin a second time."""
        self.wheel_active = False
        self.popup_win_2nd = tk.Toplevel()
        self.popup_win_2nd.wm_title('Play again?')
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        self.popup_win_2nd.geometry(f'520x360+{parent_x + 200}+{parent_y + 200}')
        message = (f'Player {self.current_player + 1} your current score is '
                   f'{self.player_scores[self.current_player]}!\n'
                   'Do you want to play again?')
        score_lbl = tk.Label(self.popup_win_2nd, text=message, 
                             font=('Tahoma', '14'), pady=70, anchor='n', 
                             width=50)
        score_lbl.grid(row=0, column=0, columnspan=2)
        yes_btn = tk.Button(self.popup_win_2nd, text='Yes', 
                            font=('Tahoma', '12', 'bold'), pady=5, padx=30,
                            command=self.yes_second_spin)
        yes_btn.grid(row=1, column=0)
        no_btn = tk.Button(self.popup_win_2nd, text='No',
                           font=('Tahoma', '12', 'bold'), pady=5, padx=30,
                           command=self.no_second_spin)
        no_btn.grid(row=1, column=1)
        self.popup_win_2nd.protocol('WM_DELETE_WINDOW', self.no_second_spin)

    def yes_second_spin(self):
        """Action to take when player wants to spin the wheel a second time."""
        self.current_spin = 1
        self.popup_win_2nd.destroy()
        self.wheel_active = True
        
    def no_second_spin(self):
        """Action to take when player does not want to play again."""
        self.display_total()
        self.show_player_total = True
        self.popup_win_2nd.destroy()
        if self.current_player < 2:
            self.display_game_popup()
            self.update_game_txt()
            self.current_player += 1
        else:   
            self.end_game()
        

    def end_game(self):
        """After all three players have played display winner."""
        self.determine_winner()
        self.game_finished = True
        self.wheel_active = False
        self.game_play_txt.delete('1.0', 'end')
        if len(self.winners) == 1:
            text = f'Winner is player {self.winners[0] + 1}'
        else:
            text = 'There is a tie!'
        self.game_play_txt.insert('1.0', text)
        self.game_over_popup()

    def determine_winner(self):
        """Determine who is the winner or winners."""
        for i in range(len(self.player_scores)):  # Check who went over 100
            if self.player_scores[i] > 100:
                self.player_scores[i] = 0
        winner_score = max(self.player_scores)
        self.winners = []
        for i in range(len(self.player_scores)):
            if self.player_scores[i] == winner_score:
                self.winners.append(i)

    def update_game_txt(self):
        """Update text box with small instructions about game."""
        self.game_play_txt.delete('1.0', 'end')
        player_total = self.player_scores[self.current_player]
        color = 'green'
        if player_total > 100 and self.show_player_total:
            color = 'red'
        self.game_play_txt.config(fg=color)
        if self.show_player_total:
            text = f'Player {self.current_player + 1} total: {player_total}!'
        else:
            text = f'Player {self.current_player + 1} spin the wheel!'
        self.game_play_txt.insert('1.0', text)

    def game_over_popup(self):
        """Display a popup at the end of the game, displaying winner, and 2 
        options: play again and exit"""
        self.popup_gameover = tk.Toplevel()
        self.popup_gameover.wm_title('Play again?')
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        self.popup_gameover.geometry(f'520x360+{parent_x + 200}+{parent_y + 200}')
        if len(self.winners) == 1:
            message = (f'Winner is player {self.winners[0] + 1}!\n'
                       'Congratulations!')
        else:
            message = 'There is a tie!'
        message_lbl = tk.Label(self.popup_gameover, text=message, font=('Tahoma', '16'), width=42, pady=75)
        message_lbl.grid(row=0, column=0, columnspan=2)
        play_btn = tk.Button(self.popup_gameover, text='Play Again', font=('Tahoma', '12', 'bold'), pady=5, width=12,
                             command=self.play_again)
        play_btn.grid(row=1, column=0)
        exit_btn = tk.Button(self.popup_gameover, text='Exit', font=('Tahoma', '12', 'bold'), pady=5, width=12,
                             command=sys.exit)
        exit_btn.grid(row=1, column=1)
        self.popup_gameover.protocol('WM_DELETE_WINDOW', sys.exit)

def main():
    """Start here."""
    root = tk.Tk()
    root.title("The Price is Right")
    root.geometry('1345x760')
    game = Game(root)
    root.mainloop()

if __name__ == '__main__':
    main()