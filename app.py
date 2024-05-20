from Board import Board
from Deck import Deck
import tkinter as tk

class MyMenu:
    def __init__(self, app):
        self.app = app
        self.menubar = tk.Menu(self.app.window)
        self.menu = tk.Menu(self.menubar, tearoff=0)
        self.NewGameMenu = tk.Menu(self.menu, tearoff=0)
        self.LeaderboardMenu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='New Game', menu=self.NewGameMenu)
        self.menu.add_command(label='Restart', command=self.app.restart)
        self.menu.add_separator()
        self.menu.add_cascade(label='Leaderboard', menu=self.LeaderboardMenu)
        self.menubar.add_cascade(label='Game', menu=self.menu)
        self.NewGameMenu.add_radiobutton(label='One Color',
                                              command=self.app.beginner)
        self.NewGameMenu.add_radiobutton(label='Two Colors',
                                              command=self.app.intermediate)
        self.NewGameMenu.add_radiobutton(label='Four Colors',
                                              command=self.app.expert)
        self.LeaderboardMenu.add_command(label='Show Leaderboard',
                                              command=self.app.show_leaderboard)
        self.LeaderboardMenu.add_command(label='Clear Leaderboard',
                                              command=self.app.reset_leaderboard)


# main class which will realize whole game:


class App:
    def __init__(self):
        self.window = tk.Tk()
        # by default level will be expert
        #self.space_label = Label(self.upper_frame, width=100)
        #self.space_label.grid(row=0, column=1)
        #self.timer = Timer(self.upper_frame)
        #self.board = Board(30, 480, 99, self.board_frame, self.timer, self.mine_counter)
        self.menu = MyMenu(self)
        self.window.config(menu=self.menu.menubar)
        self.board = Board(self.window, 4)
        self.window.mainloop()

# commands to crete new game on certain levels
    def beginner(self):
        self.board.canvas.destroy()
        self.board = Board(self.window, 1)
        #self.space_label = Label(self.upper_frame, width=10)
        #self.space_label.grid(row=0, column=1)
        #self.mine_counter.restart(10)
        #self.board.stop_threads = True
        #self.timer.stop_threads = True
        #self.timer.label.destroy()
        #self.timer = Timer(self.upper_frame)
        #self.board.timer = self.timer
        #self.board.board.destroy()
        #self.board = Board(8, 64, 10, self.board_frame, self.timer, self.mine_counter)

    def intermediate(self):
        self.board.canvas.destroy()
        self.board = Board(self.window, 2)
        #self.space_label.destroy()
        #self.space_label = Label(self.upper_frame, width=40)
        #self.space_label.grid(row=0, column=1)
        #self.mine_counter.restart(40)
        #self.board.stop_threads = True
        #self.timer.stop_threads = True
        #self.timer.label.destroy()
        #self.timer = Timer(self.upper_frame)
        #self.board.timer = self.timer
        #self.board.board.destroy()
        #self.board = Board(16, 256, 40, self.board_frame, self.timer, self.mine_counter)

    def expert(self):
        self.board.canvas.destroy()
        self.board = Board(self.window, 4)
        #self.space_label.destroy()
        #self.space_label = Label(self.upper_frame, width=100)
        #self.space_label.grid(row=0, column=1)
        #self.mine_counter.restart(99)
        #self.board.stop_threads = True
        #self.timer.stop_threads = True
        #self.timer.label.destroy()
        #self.timer = Timer(self.upper_frame)
        #self.board.timer = self.timer
        #self.board.board.destroy()
        #self.board = Board(30, 480, 99, self.board_frame, self.timer, self.mine_counter)

# restarting last game (as long as you won't click on bomb in first move)
    def restart(self):
        None
        #self.mine_counter.restart(self.board.number_of_mines)
        #self.board.stop_threads = True
        #self.timer.stop_threads = True
        #self.timer.label.destroy()
        #self.timer = Timer(self.upper_frame)
        #self.board.timer = self.timer
        #self.board.unshow()

    def reset_leaderboard(self):
        None
        #f = open("score.txt", mode='w')
        #f.write('-1\n')
        #f.write('0\n')
        #f.write('0\n')
        #f.write('-1\n')
        #f.write('0\n')
        #f.write('0\n')
        #f.write('-1\n')
        #f.write('0\n')
        #f.write('0\n')
        #f.close()
        #self.board.beginner_score = self.board.intermediate_score =\
            #self.board.expert_score = -1
        #self.board.beginner_wins = self.board.intermediate_wins=\
            #self.board.expert_wins = 0
        #self.board.beginner_loses = self.board.intermediate_loses =\
            #self.board.expert_loses = 0

    def show_leaderboard(self):
        None
        # check if there is any set score
        #if self.board.beginner_score >= 0:
            #beginner_score = self.board.beginner_score
            #beginner_percent = int(self.board.beginner_wins /\
            #(self.board.beginner_wins + self.board.beginner_loses) * 100)
        #else:
            #beginner_score = "no set times"
            #beginner_percent = 0
        #if self.board.intermediate_score >= 0:
            #intermediate_score = self.board.intermediate_score
            #intermediate_percent = int(self.board.intermediate_wins /\
            #(self.board.intermediate_wins + self.board.intermediate_loses) * 100)
        #else:
            #intermediate_score = "no set times"
            #intermediate_percent = 0
        #if self.board.expert_score >= 0:
            #expert_score = self.board.expert_score
            #expert_percent = int(self.board.expert_wins /\
            #(self.board.expert_wins + self.board.expert_loses) * 100)
        #else:
            #expert_score = "no set times"
            #expert_percent = 0
        #text = "Beginner:\nBest time: " + str(beginner_score) +\
            #"\n" + str(beginner_percent) + "% of wins\n"+\
            #"\nIntermediate:\nBest time: " + str(intermediate_score) + \
            #"\n" + str(intermediate_percent) + "% of wins\n" + \
            #"\nExpert:\nBest time: " + str(expert_score) + \
            #"\n" + str(expert_percent) + "% of wins\n"
        #messagebox.showinfo(title="LEADERBOARD", message=text)


app = App()