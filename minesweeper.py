from random import randint
from random import *
from tkinter import *
from tkinter.messagebox import showinfo
import time


class GameBoard:
    COLORS = ["black", "blue", "green", "red", "purple",
              "orange", "yellow", "pink", "brown"]
    BASE_BACKGROUND = "lawn green"
    OPEN_BACKGROUND = "tan"
    DEFAULT_DENSITY = 0.15
    BOMB_SYMBOL = "*"
    BOMB_COLOR  = "red"
    BOMB_BACKGROUND  = "pink"
    OPEN_SYMBOL = " "
    FLAG_SYMBOL = "?"
    # BOMB_DENSITY = 0.4


    FONT = ("courier", 10, "bold")

    def __init__(self, rows, columns, density=DEFAULT_DENSITY):
        self.window = Tk()
        self.rows = rows

        self.columns = columns
        self.density = density
        self.surroundingMap = {}
        self.num_bombs = (self.rows * self.columns) * self.density
        # print(self.num_bombs)
        self.window.geometry("400x400")
        self.mainFrame = Frame(self.window, highlightbackground="brown", highlightthickness=2)
        self.mainFrame.pack(expand=True, fill="both")

        self.headerFrame = Frame(self.mainFrame)
        self.headerFrame.pack(fill="x")

        self.timeLabel = Label(self.headerFrame, text="", font=("courier", 15, "bold"))
        self.timeLabel.grid(row=0, column=2)

        self.current_flags = IntVar(self.mainFrame)
        self.current_flags.set(0)

        Label(self.headerFrame, text="Flags Placed:", font=("courier", 15, "bold")).grid(row=0, column=0)
        self.flagsLabel = Label(self.headerFrame, textvariable=self.current_flags, font=("courier", 15, "bold"))
        self.flagsLabel.grid(row=0, column=1)

        Label(self.headerFrame, text=f"Number of Bombs: {self.num_bombs}", font=("courier", 15, "bold")).grid(row=0, column=3)

        self.headerFrame.grid_columnconfigure((2,3), weight=1)



        self.buildBoard()

        for row in self.bboard:
            for tup in row:
                button = tup[0]
                button.bind("<Button-3>", self.create_placeFlag_handler(button))

        for row in self.bboard:
            for tup in row:
                button = tup[0]
                coord = tup[1]
                button.bind("<Button-1>", self.create_revealNumber_handler(button, coord))

        self.generateBombs()
        self.calculateNumbers()


        self.start_time = time.time()
        self.start_timer()



    def update_time(self):
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        minutes = int(elapsed_time //60)
        seconds = int(elapsed_time % 60)
        time_str = f"{minutes:02d}:{seconds:02d}"
        self.timeLabel.config(text=time_str)
        self.after_id = self.mainFrame.after(1000, self.update_time)

    def start_timer(self):
        self.update_time()

    def buildBoard(self):
        board = []
        self.bboard = []
        # print(self.rows)

        for frow in range(0, self.rows):
            frame_element = Frame(self.mainFrame)
            frame_element.pack(fill="both", expand=True)
            frame_row = [frame_element]
            board.append(frame_row)
            self.bboard.append([])
            for column in range(0, self.columns):
                frame = board[frow][0]
                button = Button(frame, bg=GameBoard.BASE_BACKGROUND, width=1, text=" ")
                # button.bind("<Button-3>", self.placeFlag)
                # button.bind("<Button-1>", self.revealNumber)
                button.pack(side="left", fill="both", expand=True)  # set sticky property
                self.bboard[frow].append((button, [frow, column]))



    def create_placeFlag_handler(self, button):
        def placeFlag_handler(event):
            self.placeFlag(event, button)

        return placeFlag_handler

    def placeFlag(self, event, button: Button):
        state = button.cget("text")
        current_num = self.current_flags.get()
        if state == "🚩":
            button.config(text="")
            self.current_flags.set(current_num - 1)
        else:
            print(f"Changing {button} to flag")
            button.config(text="🚩", fg="red")
            self.current_flags.set(current_num + 1)
        print(self.current_flags.get())

    def create_revealNumber_handler(self, button, coord):
        def revealNumber_handler(event):
            if coord[0] != 0:
                self.revealNumber(event, button, coord)
            else:
                self.revealNumber(event, button, coord, smart=False)

        return revealNumber_handler

    def revealNumber(self, event, button: Button, coord, smart=True):
        # reveal button and check if it's a bomb
        try:
            button.config(text=self.surroundingMap[tuple(coord)])
            button.config(bg=GameBoard.OPEN_BACKGROUND)
            if self.surroundingMap[tuple(coord)] == 0:
                button.config(text=" ")
            if self.surroundingMap[tuple(coord)] == 1:
                button.config(fg="blue")
            elif self.surroundingMap[tuple(coord)] == 2:
                button.config(fg="green")
            elif self.surroundingMap[tuple(coord)] == 3:
                button.config(fg="#eb3438")

        except KeyError as e:
            button.config(text="💣")
            button.config(fg="purple")
            button.config(bg=GameBoard.BOMB_BACKGROUND)
            self.headerFrame.pack_forget()
            self.endgame()


        # if the button is not a bomb and smart flag is True, perform smart click
        try:
            if smart and self.surroundingMap[tuple(coord)] == 0:
                row = coord[0]
                column = coord[1]
                above = [self.bboard[row][column][1][0] - 1, self.bboard[row][column][1][1]]  # subtract 1 row
                below = [self.bboard[row][column][1][0] + 1, self.bboard[row][column][1][1]]  # add 1 row
                left = [self.bboard[row][column][1][0], self.bboard[row][column][1][1] - 1]  # subtract 1 column
                right = [self.bboard[row][column][1][0], self.bboard[row][column][1][1] + 1]  # add 1 column
                dlt = [self.bboard[row][column][1][0] - 1,
                       self.bboard[row][column][1][1] - 1]  # subtract row, subtract column
                drt = [self.bboard[row][column][1][0] - 1, self.bboard[row][column][1][1] + 1]  # subtract row, add column
                dlb = [self.bboard[row][column][1][0] + 1, self.bboard[row][column][1][1] - 1]  # add row, subtract column
                drb = [self.bboard[row][column][1][0] + 1, self.bboard[row][column][1][1] + 1]  # add row, add column
                sur_buttons = [above, below, left, right, dlt, drt, dlb, drb]

                for coordinate in sur_buttons:
                    try:
                        button_sur = self.bboard[coordinate[0]][coordinate[1]][0]
                        if coordinate in self.bomb_array:
                            continue
                        else:
                            # recursively call revealNumber with smart flag set to False
                            self.revealNumber(None, button_sur, coordinate, smart=False)
                    except IndexError:
                        pass
        except KeyError:
            print("GAME OVER")

    def endgame(self):
        for bomb_coord in self.bomb_array:
            self.bboard[bomb_coord[0]][bomb_coord[1]][0].config(text="💣")
            self.bboard[bomb_coord[0]][bomb_coord[1]][0].config(fg="#2f1d5a")
            self.bboard[bomb_coord[0]][bomb_coord[1]][0].config(bg=GameBoard.BOMB_BACKGROUND)

        for row in self.bboard:
            for tup in row:
                print(tup)
                button = tup[0]
                coord = tup[1]
                try:
                    button.config(text=self.surroundingMap[tuple(coord)])
                    button.unbind("<Button-1>")
                    button.unbind("<Button-3>")
                except KeyError as e:
                    pass

        for row in self.bboard:
            for tup in row:
                print(tup)
                button = tup[0]
                coord = tup[1]
                if coord in self.bomb_array:
                    button.unbind("<Button-1>")
                    button.unbind("<Button-3>")

        Label(self.mainFrame, text="GAME OVER", font=("courier", 15, "bold")).pack()
        Button(self.mainFrame, text="Play Again", font=("courier", 15, "bold"), command=self.newGame).pack()

    def newGame(self):
        newGame = GameBoard(self.rows, self.columns)
        self.window.destroy()
        newGame.display()


    def smartClick(self, button, coord):
        row = coord[0]
        column = coord[1]
        above = [self.bboard[row][column][1][0] - 1, self.bboard[row][column][1][1]]  # subtract 1 row
        below = [self.bboard[row][column][1][0] + 1, self.bboard[row][column][1][1]]  # add 1 row
        left = [self.bboard[row][column][1][0], self.bboard[row][column][1][1] - 1]  # subtract 1 column
        right = [self.bboard[row][column][1][0], self.bboard[row][column][1][1] + 1]  # add 1 column
        dlt = [self.bboard[row][column][1][0] - 1, self.bboard[row][column][1][1] - 1]  # subtract row, subtract column
        drt = [self.bboard[row][column][1][0] - 1, self.bboard[row][column][1][1] + 1]  # subtract row, add column
        dlb = [self.bboard[row][column][1][0] + 1, self.bboard[row][column][1][1] - 1]  # add row, subtract column
        drb = [self.bboard[row][column][1][0] + 1, self.bboard[row][column][1][1] + 1]  # add row, add column
        sur_buttons = [above, below, left, right, dlt, drt, dlb, drb]

        for coordinate in sur_buttons:
            row, col = coordinate
            if row >= 0 and row < self.rows and col >= 0 and col < self.columns:
                button_obj = self.bboard[row][col][0]
                if coordinate in self.bomb_array:
                    break
                elif self.surroundingMap[tuple(coordinate)] == 0 and button_obj.cget("state") != "disabled":
                    button_obj.config(state="disabled", bg=GameBoard.OPEN_BACKGROUND)
                    self.smartClick(button_obj, coordinate)
                else:
                    self.revealNumber(None, button_obj, coordinate)

    def get_neighbors(self, row, col):
        # Define the list of neighboring coordinates as offsets
        offsets = [(-1, -1), (-1, 0), (-1, 1),
                   (0, -1), (0, 1),
                   (1, -1), (1, 0), (1, 1)]

        # Generate a list of coordinates of neighboring cells by adding the offsets
        neighbors = [(row + dr, col + dc) for dr, dc in offsets]

        # Return a list of neighboring coordinates that fall within the bounds of the game board
        in_bounds_neighbors = [(r, c) for r, c in neighbors
                               if 0 <= r < self.rows and 0 <= c < self.columns]

        return in_bounds_neighbors

    def generateBombs(self):
        self.bomb_array = []
        while len(self.bomb_array) != int(self.num_bombs):
            random_row = randrange(0, self.rows)
            random_column = randrange(0, self.columns)
            if [random_row, random_column] in self.bomb_array:
                pass
            else:
                self.bomb_array.append([random_row, random_column])

        # print(self.bomb_array)

    def calculateNumbers(self):
        for row in self.bboard:
            for tup in row:
                button_coord = tup[1]
                if button_coord in self.bomb_array:
                    pass
                    # print(f"{button_coord} is a bomb")
                else:
                    button_object = tup[0]
                    self.buildButtonNumber((button_coord, button_object))

    def buildButtonNumber(self, button_info : tuple):
        row = button_info[0][0]
        column = button_info[0][1]
        # print(row, column)

        above = [self.bboard[row][column][1][0] - 1, self.bboard[row][column][1][1]] # subtract 1 row
        below = [self.bboard[row][column][1][0] + 1, self.bboard[row][column][1][1]] # add 1 row
        left = [self.bboard[row][column][1][0], self.bboard[row][column][1][1] - 1] # subtract 1 column
        right = [self.bboard[row][column][1][0], self.bboard[row][column][1][1] + 1] # add 1 column
        dlt = [self.bboard[row][column][1][0] - 1, self.bboard[row][column][1][1] - 1] # subtract row, subtract column
        drt = [self.bboard[row][column][1][0] - 1, self.bboard[row][column][1][1] + 1] # subtract row, add column
        dlb = [self.bboard[row][column][1][0] + 1, self.bboard[row][column][1][1] - 1] # add row, subtract column
        drb = [self.bboard[row][column][1][0] + 1, self.bboard[row][column][1][1] + 1] # add row, add column
        sur_buttons = [(button_info[1]), above, below, left, right, dlt, drt, dlb, drb]

        surrounding_bomb_count = 0
        for button in sur_buttons:
            # print(self.bomb_array)
            # print(sur_buttons)
            if button in self.bomb_array:
                surrounding_bomb_count += 1
            else:
                pass
                # print("False")
        # print(sur_buttons[0], f"has {surrounding_bomb_count} next to it.")
        self.surroundingMap[tuple(button_info[0])] = surrounding_bomb_count
        # print("__________________________________________________")



    def display(self):
        self.window.geometry("600x600")
        self.window.mainloop()

        # print("displaying")
#=========================================================================================
# Testing code below - DO NOT MODIFY

# Only run this code below if this is called as the main, not imported
if __name__ == '__main__':
    import sys
    sys.path.append('..')
    from utils.ledger import grab
    FILE = "minesweeper"
    grab(FILE)
    board = GameBoard(20, 20)
    board.display()


