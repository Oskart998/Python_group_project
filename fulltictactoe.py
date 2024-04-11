import csv
import os
import tkinter as tk
from tkinter import PhotoImage
from breezypythongui import EasyFrame
from tkinter import font
from TicTacToe import TicTacToe

class GameBoard(EasyFrame):
    def __init__(self, title="Tic Tac Toe"):
        super().__init__(title=title)
        self.player1Name = self.getUserNames(1).ljust(8)
        self.player2Name = self.getUserNames(2).ljust(8)
        self.currentPlayer = self.player1Name
        self.game = TicTacToe()
        self.player1wins = 0
        self.player2wins = 0
        self.avatar1Image = None
        self.avatar2Image = None
        self.users_file_path = "users.csv"
        purpleHex = "#8916a6"
        
        self.firstPlayerImg = self.addLabel(text="", row=1, column=1, sticky="NSEW"
                                            ,background=purpleHex)
        self.secondPlayerImg = self.addLabel(text="", row=1, column=3, sticky="NSEW",
                                             background=purpleHex)


        self.selectAvatar()
        
        
        self.setBackground(purpleHex)
        self.setSize(550, 700)
        self.setResizable(False)
        consoleFont = font.Font(family="Lucida Console", size=8, font=font.BOLD)

        self.addLabel(text=f"Player 1: {self.player1Name}", row=0, column=0, sticky="NSEW", columnspan=2,
                      background=purpleHex,  font= consoleFont)
        self.addLabel(text=f"Player 2: {self.player2Name}", row=0, column=3, sticky="NSEW", columnspan=2,
                      background=purpleHex, font= consoleFont)
       

        self.player1WinsLabel = self.addLabel(text=f"Wins: {self.player1wins}", row=2, column=0, sticky="NSEW",
                      background=purpleHex, font=consoleFont, columnspan=2)
        
        self.player2WinsLabel = self.addLabel(text=f"Wins: {self.player2wins}", row=2, column=3, sticky="NSEW",
                      background=purpleHex, font=consoleFont, columnspan=2)

        self.turnLabel = self.addLabel(text=f"Current player: {self.currentPlayer}", row=3, column=2,
                                       background=purpleHex, sticky="NSEW", font= consoleFont)

        self.controlPanel = self.addPanel(background="#4b494d", row=4, column=0, columnspan=4,
                                          rowspan=3)
        self.controlPanel.buttons = []
        for row in range(4, 7):
            for col in range(1, 4):
                button = self.addButton(text="", row=row, column=col)
                button.config(background="#cc71e3",width=100, height=100, command=lambda btn=button, row=row-4, col=col-1: self.makeMove(btn, row, col))
                self.controlPanel.buttons.append(button)
        
        self.images = []

        for i in range(len(self.controlPanel.buttons)):
                self.images.append(PhotoImage(width=100, height=100))
                self.controlPanel.buttons[i]["image"] = self.images[i]

        self.image1 = PhotoImage(file="xx.gif")
        self.image2 = PhotoImage(file="o.gif")


    def getUserNames(self, playerNum):
        return self.prompterBox(title="Player Info", promptString=f"Enter Player {playerNum} name")
        
    def selectAvatar(self):
        self.closedCount = 0
        self.avatars = []

        for i in range(1, 5):
                image = PhotoImage(file=f"av{i}.gif", width=100, height=100)
                self.avatars.append([image, f"av{i}.gif"])

        self.master.withdraw()
        self.createWindows()

    def createWindows(self):
        avatar1 = self.get_user_avatar(self.player1Name)
        avatar2 = self.get_user_avatar(self.player2Name)
        coordinates = [(0,0), (0, 1), (1, 0), (1, 1)]
        consoleFont = font.Font(family="Lucida Console", size=8, font=font.BOLD)

        if avatar1 == None:
            self.frameAvatar1 = tk.Toplevel()
            self.avatar1Btns = []

            tk.Label(self.frameAvatar1,text=f"Select an avatar for {self.player1Name}", font=consoleFont).grid(row= 0, column=0, columnspan=2)
            
            for i in range(4):
                self.avatar1Btns.append(tk.Button(self.frameAvatar1, text="", command=lambda i=i: self.hideWind(self.avatar1Btns[i], 1, i),
                                                image=self.avatars[i][0]))

                self.avatar1Btns[i].image = self.avatars[i]

                self.avatar1Btns[i].grid(row= coordinates[i][0]+1, column = coordinates[i][1])
        
        else:
             self.closedCount += 1
             self.hideWind(None, 3, 0)
             self.firstImage = PhotoImage(file=avatar1)
             self.firstPlayerImg["image"] = self.firstImage

        if avatar2 == None:
            self.frameAvatar2 = tk.Toplevel()  
            self.avatar2Btns = []                                                                                                                   
            tk.Label(self.frameAvatar2,text=f"Select an avatar for {self.player2Name}", font=consoleFont).grid(row = 0, column= 0,
                                                                                                               columnspan=2)

            for i in range(4):
                
                self.avatar2Btns.append(tk.Button(self.frameAvatar2, text="", command=lambda i=i: self.hideWind(self.avatar2Btns[i], 2, i),
                                                image=self.avatars[i][0]))

                # Keep a reference to the image to prevent it from being garbage collected
                
                self.avatar2Btns[i].image = self.avatars[i]

                #self.avatar1Btns[i].pack()
                #self.avatar2Btns[i].pack()
                self.avatar2Btns[i].grid(row= coordinates[i][0]+1, column = coordinates[i][1])
              
        else:
            self.closedCount += 1
            self.hideWind(None, 3, 0)
            self.secondImage = PhotoImage(file=avatar2)
            self.secondPlayerImg["image"] = self.secondImage

    def hideWind(self, btn,windNum, index):
        if windNum == 1:
            self.write_csv([self.player1Name, self.avatars[index][1], 0])
            self.avatar1Image = btn.cget("image")
            self.firstImage = self.avatar1Image
            self.firstPlayerImg["image"] = self.firstImage
            self.frameAvatar1.destroy()    
            self.closedCount += 1

        elif windNum == 2:
            self.write_csv([self.player2Name, self.avatars[index][1], 0])
            self.avatar2Image = btn.cget("image")
            self.secondImage = self.avatar2Image
            self.secondPlayerImg["image"] = self.secondImage
            self.frameAvatar2.destroy()
            self.closedCount += 1


        if self.closedCount == 2:
            self.master.deiconify()
           

    def write_csv(self, data):
        with open(self.users_file_path, 'a', newline='') as csvfile:
            csvWriter = csv.writer(csvfile)
            csvWriter.writerow(data) 

    def get_user_avatar(self, playerName):
        with open(self.users_file_path, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if playerName in row:
                    # Assuming the second column is at index 1 (0-based indexing)
                    return row[1]  # Return the value of the second column
        return None  # Return None if the target string is not found


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
        



    def makeMove(self, btn, row, col):
        if self.game.make_move(row, col):
            if self.currentPlayer == self.player1Name:
                btn.config(image=self.image1)
                self.currentPlayer = self.player2Name
            else:
                btn.config(image=self.image2)
                self.currentPlayer = self.player1Name
            
            self.turnLabel.config(text=f"Current player: {self.currentPlayer}")

            winner = self.game.check_winner()
            if winner:
                if winner == self.player1Name:
                    self.player1wins += 1
                elif winner == self.player2wins:
                    self.player2wins += 1
                self.showWinner(winner)


    def resetGameBoard(self):

        for i in range(len(self.controlPanel.buttons)):
                self.images.append(PhotoImage(width=100, height=100))
                self.controlPanel.buttons[i]["image"] = self.images[i]
                
    
    def showWinner(self, winner):
        if winner == 'Draw':
            tk.messagebox.showinfo("Game Over", "It's a draw!")
        else:
            winnerName = f"{self.player1Name}" if winner == 'X' \
                            else f"{self.player2Name}"
            if winner == "X":
                self.player1wins += 1
                self.player1WinsLabel["text"] = "Wins:" + str(self.player1wins)
            else:
                self.player2wins += 1
                self.player2WinsLabel["text"] = "Wins:" + str(self.player2wins)
                
            self.update_wins(winnerName)
            tk.messagebox.showinfo("Game Over", f"Player {winnerName.strip()} wins!")

        self.resetGameBoard()
        self.game.reset()
        self.turnLabel.config(text=f"Current player: {self.player1Name}")
        self.currentPlayer = self.player1Name



def main():
    GameBoard().mainloop()

if __name__ == "__main__":
    main()
