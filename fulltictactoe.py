import csv
import os
import tkinter as tk
from tkinter import PhotoImage
from breezypythongui import EasyFrame
from tkinter import font
from TicTacToe import TicTacToe
import random

class GameBoard(EasyFrame):
    def __init__(self, title="Tic Tac Toe"):
        super().__init__(title=title)
        mode = self.prompterBox("Enter Game Mode Player vs Player (PvP) or Player vs Computer (Computer)")
        self.mode = mode
        self.setup_game()
        self.current_player = self.player1_name
        self.setup_ui()
        self.game_over = False  # Initialize game_over attribute

    def setup_game(self):
        # Set up the game by initializing player names and game state
        self.player1_name = self.prompterBox(title="Player Info", promptString="Enter Player 1 name").ljust(8)
        self.player2_name = self.prompterBox(title="Player Info", promptString="Enter Player 2 name").ljust(8) if self.mode == 'PvP' else "Computer"
        self.game = TicTacToe(against_computer=(self.mode == 'Computer'))
        self.player1_wins = 0
        self.player2_wins = 0
        self.avatar1_image = None
        self.avatar2_image = None
        self.users_file_path = "users.csv"

    def setup_ui(self):
        # Set up the user interface
        purple_hex = "#8916a6"
        self.first_player_img = self.addLabel(text="", row=1, column=1, sticky="NSEW", background=purple_hex)
        self.second_player_img = self.addLabel(text="", row=1, column=3, sticky="NSEW", background=purple_hex)
        self.choose_avatar()
        self.setBackground(purple_hex)
        self.setSize(550, 700)
        self.setResizable(False)
        console_font = font.Font(family="Lucida Console", size=8, font=font.BOLD)
        self.display_player_info(console_font)
        self.setup_buttons()



    def choose_avatar(self):
        # Allow players to choose their avatars
        self.closed_count = 0
        self.avatars = []

        for i in range(1, 5):
            image = PhotoImage(file=f"av{i}.gif", width=100, height=100)
            self.avatars.append([image, f"av{i}.gif"])

        self.master.withdraw()
        self.setup_windows()

    def setup_windows(self):
        # Create avatar selection windows
        avatar1 = self.get_user_avatar(self.player1_name)
        avatar2 = self.get_user_avatar(self.player2_name)
        coordinates = [(0,0), (0, 1), (1, 0), (1, 1)]
        console_font = font.Font(family="Lucida Console", size=8, font=font.BOLD)

        if avatar1 == None:
            self.frame_avatar1 = tk.Toplevel()
            self.avatar1_btns = []

            tk.Label(self.frame_avatar1,text=f"Select an avatar for {self.player1_name}", font=console_font).grid(row= 0, column=0, columnspan=2)

            for i in range(4):
                self.avatar1_btns.append(tk.Button(self.frame_avatar1, text="", command=lambda i=i: self.hide_window(self.avatar1_btns[i], 1, i),
                                                image=self.avatars[i][0]))

                self.avatar1_btns[i].image = self.avatars[i]
                self.avatar1_btns[i].grid(row= coordinates[i][0]+1, column = coordinates[i][1])

        else:
             self.closed_count += 1
             self.hide_window(None, 3, 0)
             self.first_image = PhotoImage(file=avatar1)
             self.first_player_img["image"] = self.first_image

        if avatar2 == None:
            self.frame_avatar2 = tk.Toplevel()
            self.avatar2_btns = []
            tk.Label(self.frame_avatar2,text=f"Select an avatar for {self.player2_name}", font=console_font).grid(row = 0, column= 0, columnspan=2)

            for i in range(4):
                self.avatar2_btns.append(tk.Button(self.frame_avatar2, text="", command=lambda i=i: self.hide_window(self.avatar2_btns[i], 2, i),
                                                image=self.avatars[i][0]))

                self.avatar2_btns[i].image = self.avatars[i]
                self.avatar2_btns[i].grid(row= coordinates[i][0]+1, column = coordinates[i][1])

        else:
            self.closed_count += 1
            self.hide_window(None, 3, 0)
            self.second_image = PhotoImage(file=avatar2)
            self.second_player_img["image"] = self.second_image

    def hide_window(self, btn, wind_num, index):
        # Hide avatar selection window after selection
        if wind_num == 1:
            self.write_csv([self.player1_name, self.avatars[index][1], 0])
            self.avatar1_image = btn.cget("image")
            self.first_image = self.avatar1_image
            self.first_player_img["image"] = self.first_image
            self.frame_avatar1.destroy()
            self.closed_count += 1

        elif wind_num == 2:
            self.write_csv([self.player2_name, self.avatars[index][1], 0])
            self.avatar2_image = btn.cget("image")
            self.second_image = self.avatar2_image
            self.second_player_img["image"] = self.second_image
            self.frame_avatar2.destroy()
            self.closed_count += 1

        if self.closed_count == 2:
            self.master.deiconify()

    def write_csv(self, data):
        # Write user avatar selection to CSV file
        with open(self.users_file_path, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(data)

    def get_user_avatar(self, playerName):
        # Get user avatar from CSV file
        with open(self.users_file_path, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if playerName in row:
                    return row[1]
        return None

    def display_player_info(self, console_font):
        # Display player names and win counts
        self.addLabel(text=f"P1: {self.player1_name}", row=0, column=0, sticky="NSEW", columnspan=2,
                      background="#8916a6", font= console_font)
        self.addLabel(text=f"P2: {self.player2_name}", row=0, column=3, sticky="NSEW", columnspan=2,
                      background="#8916a6", font= console_font)
        self.player1_wins_label = self.addLabel(text=f"Wins: {self.player1_wins}", row=2, column=0, sticky="NSEW",
                      background="#8916a6", font=console_font, columnspan=2)
        self.player2_wins_label = self.addLabel(text=f"Wins: {self.player2_wins}", row=2, column=3, sticky="NSEW",
                      background="#8916a6", font=console_font, columnspan=2)
        self.turn_label = self.addLabel(text=f"Current player: {self.current_player}", row=3, column=2,
                                       background="#8916a6", sticky="NSEW", font= console_font)

    def setup_buttons(self):
        # Set up game control buttons
        self.control_panel = self.addPanel(background="#4b494d", row=4, column=0, columnspan=4,
                                          rowspan=3)
        self.control_panel.buttons = []
        for row in range(4, 7):
            for col in range(1, 4):
                button = self.addButton(text="", row=row, column=col)
                button.config(background="#cc71e3",width=100, height=100, command=lambda btn=button, row=row-4, col=col-1: self.make_move(btn, row, col))
                self.control_panel.buttons.append(button)
        
        self.images = []

        # Load images for game buttons
        for i in range(len(self.control_panel.buttons)):
                self.images.append(PhotoImage(width=100, height=100))
                self.control_panel.buttons[i]["image"] = self.images[i]

        self.image1 = PhotoImage(file="xx.gif")
        self.image2 = PhotoImage(file="o.gif")

     # Update user wins in CSV file
    def update_wins(self, winner):
        # Temporary file to store updated rows
        temp_file_path = self.users_file_path + '.tmp'

        # Open the CSV file for reading and writing
        with open(self.users_file_path, 'r', newline='') as csvfile, \
            open(temp_file_path, 'w', newline='') as temp_file:

            csvreader = csv.reader(csvfile)
            csvwriter = csv.writer(temp_file)

            # Iterate through rows and update wins if winner is found
            for row in csvreader:
                if winner in row:
                    row[2] = str(int(row[2]) + 1)  # Increment wins

                # Write the row to the temporary file
                csvwriter.writerow(row)

        # Replace the original file with the temporary file
        os.replace(temp_file_path, self.users_file_path)
    
    def make_move(self, btn, row, col):
        if self.game_over:
            return

        if self.game.make_move(row, col):
            if self.current_player == self.player1_name:
                btn.config(image=self.image1)
                self.current_player = self.player2_name
            else:
                btn.config(image=self.image2)
                self.current_player = self.player1_name
            
            self.turn_label.config(text=f"Current player: {self.current_player}")

            if self.mode == 'Computer' and self.current_player == self.player2_name:
                self.after(1200, self.make_computer_move)  # Delay for 2 seconds before making the computer move

            winner = self.game.check_winner()

            if winner:
                self.game_over = True
                if winner == self.player1_name:
                    self.player1_wins += 1
                elif winner == self.player2_name:
                    self.player2_wins += 1
                self.show_winner(winner)
            
        # If playing against the computer and it's the computer's turn, make its move
        

    def make_computer_move(self):
        if not self.game_over:
            row, col = self.game.make_computer_move()
            index = row * 3 + col
            button = self.control_panel.buttons[index]
            button.invoke()  # Simulate a button click to make the move


    def show_winner(self, winner):
        if winner == 'Draw':
            tk.messagebox.showinfo("Game Over", "It's a draw!")
        else:
            winner_name = f"{self.player1_name}" if winner == 'X' else f"{self.player2_name}"
            if winner == "X":
                self.player1_wins += 1
                self.player1_wins_label["text"] = "Wins:" + str(self.player1_wins)
            else:
                self.player2_wins += 1
                self.player2_wins_label["text"] = "Wins:" + str(self.player2_wins)
                
            self.update_wins(winner_name)

            tk.messagebox.showinfo("Game Over", f"Player {winner_name.strip()} wins!")

        self.reset_game_board()
        self.turn_label.config(text=f"Current player: {self.player1_name}")
        self.current_player = self.player1_name

    def reset_game_board(self):
        for i in range(len(self.control_panel.buttons)):
                self.images.append(PhotoImage(width=100, height=100))
                self.control_panel.buttons[i]["image"] = self.images[i]
                
        self.game.reset()
        self.current_player = self.player1_name
        self.turn_label.config(text=f"Current player: {self.current_player}")
        self.game_over = False

def main():
    GameBoard().mainloop()

if __name__ == "__main__":
    main()
