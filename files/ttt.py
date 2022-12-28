from tkinter import *
import tkinter.messagebox

try:
    from files import AI
except ModuleNotFoundError:
    exit("AI file not found")


class App(Tk):
    def __init__(self):
        super().__init__()

        self.ai = AI.Bot()

        window_coordx = int((self.winfo_screenwidth() - 440) / 2)
        window_coordy = int((self.winfo_screenheight() - 590) / 2)
        self.geometry(f"440x590+{window_coordx}+{window_coordy}")
        self.config(bg="black")
        self.title("Tic Tac Toe")
        self.resizable(False, False)
        self.minsize(440, 590)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        try:
            self.iconphoto(True, PhotoImage(file="files/tttlogo.png"))
        except TclError:
            pass

        # Game Attributes
        self.score_x = IntVar()
        self.score_x.set(0)
        self.playerxname = StringVar()

        self.score_o = IntVar()
        self.score_o.set(0)
        self.playeroname = StringVar()

        self.current = StringVar()
        self.current.set("X")
        self.current_color = "cyan"

        self.opponent = StringVar()  # computer OR player
        self.opponent.set("computer")
        self.difficulty = StringVar()  # easy, normal OR hard
        self.difficulty.set("normal")

        self.frozen = True
        self.clicks = 0
        self.matches = 0
        self.icons = ("X", "O")
        self.moves = ""

        temp = (7, 4, 1)
        self.board = [[[temp[i] + j, StringVar()] for j in range(3)] for i in range(3)]
        self.board_labels = []

        # GAME SCREEN WIDGETS
        self.gamescreen = Frame(self, bg="black")
        self.gamescreen.columnconfigure(0, weight=1)
        self.gamescreen.rowconfigure(1, weight=1)
        self.gamescreen.grid(row=0, column=0, sticky=NSEW)

        self.scoreframe = Frame(self.gamescreen, bg="black")

        self.turnframe = Frame(self.scoreframe, bg="black")
        self.labturn = Label(self.turnframe, text="Turn", font=('Calibri', 24), fg="white", bg="black")
        self.labturnsym = Label(self.turnframe, textvariable=self.current, font=('Calibri', 24), fg="cyan", bg="black")

        self.config_gameframe()

        # MAIN MENU SCREEN
        self.orangish = "#d86950"
        self.goldenish = "#e8b953"
        self.mainscreen = Frame(self, bg=self.goldenish)
        self.mainscreen.grid(row=0, column=0, sticky=NSEW)

        self.mainscreen.columnconfigure(0, weight=1)
        self.mainscreen.rowconfigure(2, weight=1)

        logoframe = Frame(self.mainscreen, bg=self.goldenish, height=120)
        logoframe.grid_propagate(False)
        logoframe.grid(row=0, column=0, sticky=EW)
        logoframe.columnconfigure(0, weight=1)

        try:
            logo = PhotoImage(file="files/tttlogo_smol.png")
            logolabel = Label(logoframe, image=logo, bg=self.goldenish)
        except TclError:
            try:
                logo = PhotoImage(file="tttlogo_smol.png")
                logolabel = Label(logoframe, image=logo, bg=self.goldenish)
            except TclError:
                logolabel = Label(
                    logoframe, text="TicTacToe",
                    fg=self.orangish, bg=self.goldenish,
                    font=("Segoe Script", 32, "italic", "bold")
                )

        logolabel.grid(row=0, column=0, pady=10, sticky=EW)

        playbutton = Button(
            self.mainscreen,
            text="START GAME",
            bg="maroon", fg="white",
            activebackground="brown4",
            font=("Calibri", 20, "bold"),
            padx=5,
            command=self.start_game
        )
        playbutton.grid(row=1, column=0, pady=10)

        opponentframe = Frame(self.mainscreen, bg=self.goldenish)
        opponentframe.grid(row=2, column=0, pady=10, sticky=NS)
        opponentframe.columnconfigure(0, weight=1)
        opponentframe.columnconfigure(1, weight=1)
        opponentframe.rowconfigure(7, weight=1)

        self.player2entry = Entry(opponentframe, textvariable=self.playeroname, font=("Calibri", 14))
        self.player2entry.grid(row=10, column=1, sticky=W)

        def oppo_choose():
            radio_computer.config(selectcolor="white")
            radio_2player.config(selectcolor="white")
            easy_radio.config(selectcolor="white", state=NORMAL)
            norm_radio.config(selectcolor="white", state=NORMAL)
            hard_radio.config(selectcolor="white", state=NORMAL)
            self.player2entry.config(state=NORMAL)

            if self.opponent.get() == "computer":
                self.player2entry.config(state=DISABLED)
                radio_computer.config(selectcolor="black")
                if self.difficulty.get() == "easy":
                    easy_radio.config(selectcolor="black")
                elif self.difficulty.get() == "normal":
                    norm_radio.config(selectcolor="black")
                else:
                    hard_radio.config(selectcolor="black")

                diff = self.difficulty.get()
                self.playeroname.set(f"{diff.title()}-Bot")
            else:
                self.player2entry.config(state=NORMAL)
                radio_2player.config(selectcolor="black")
                easy_radio.config(state=DISABLED)
                norm_radio.config(state=DISABLED)
                hard_radio.config(state=DISABLED)
                self.playeroname.set("Player 2")

        Label(opponentframe, text="Play Against:", font=("Calibri", 18, "bold"), bg=self.goldenish, fg="black") \
            .grid(row=0, column=0, columnspan=2, sticky=W)
        radio_2player = Radiobutton(opponentframe, text="Friend",
                                    value="player", variable=self.opponent, command=oppo_choose,
                                    bg=self.goldenish, font=("Calibri", 16), fg="black",
                                    activebackground=self.goldenish, selectcolor="white")
        radio_2player.grid(row=1, column=0, sticky=W, columnspan=2)

        radio_computer = Radiobutton(opponentframe, text="Computer",
                                     value="computer", variable=self.opponent, command=oppo_choose,
                                     bg=self.goldenish, font=("Calibri", 16), fg="black",
                                     activebackground=self.goldenish, selectcolor="black")
        radio_computer.grid(row=2, column=0, sticky=W, columnspan=2)

        Label(opponentframe, text="Difficulty:", font=("Calibri", 14, "bold"), bg=self.goldenish, fg="black") \
            .grid(row=3, column=1, sticky=W)
        easy_radio = Radiobutton(opponentframe, text="Easy",
                                 value="easy", variable=self.difficulty,
                                 command=lambda: [oppo_choose(), self.ai.easy()],
                                 bg=self.goldenish, font=("Calibri", 14), fg="black",
                                 activebackground=self.goldenish, selectcolor="white")
        easy_radio.grid(row=4, column=1, sticky=W)
        norm_radio = Radiobutton(opponentframe, text="Normal",
                                 value="normal", variable=self.difficulty,
                                 command=lambda: [oppo_choose(), self.ai.normal()],
                                 bg=self.goldenish, font=("Calibri", 14), fg="black",
                                 activebackground=self.goldenish, selectcolor="black")
        norm_radio.grid(row=5, column=1, sticky=W)
        hard_radio = Radiobutton(opponentframe, text="Hard",
                                 value="hard", variable=self.difficulty,
                                 command=lambda: [oppo_choose(), self.ai.hard()],
                                 bg=self.goldenish, font=("Calibri", 14), fg="black",
                                 activebackground=self.goldenish, selectcolor="white")
        hard_radio.grid(row=6, column=1, sticky=W)
        norm_radio.invoke()

        Frame(opponentframe, bg=self.goldenish).grid(row=7, column=0, sticky=NS)
        
        Label(opponentframe, text="Enter Usernames:", bg=self.goldenish, font=("Calibri", 12), fg="black") \
            .grid(row=8, column=0, columnspan=2, sticky=W)
        Label(opponentframe, text="Player 1 (X):", bg=self.goldenish, font=("Calibri", 14), fg="black") \
            .grid(row=9, column=0, sticky=EW)
        Entry(opponentframe, textvariable=self.playerxname, font=("Calibri", 14)) \
            .grid(row=9, column=1, sticky=W)

        Label(opponentframe, text="Player 2 (O):", bg=self.goldenish, font=("Calibri", 14), fg="black") \
            .grid(row=10, column=0, sticky=EW)
        # Player 2 entry defined above the function "oppo_choose"

        Frame(opponentframe, height=20, bg=self.goldenish).grid(row=10, column=0, sticky=NS)

        self.start_app()

    def config_gameframe(self):
        self.scoreframe.grid(row=0, column=0, sticky=EW)
        self.scoreframe.rowconfigure(0, weight=1)
        self.scoreframe.columnconfigure(2, weight=1)

        self.lab_x = Label(self.scoreframe, text="X =", font=('Calibri', 24, "bold"), fg="cyan", bg="black")
        self.lab_x.grid(row=0, column=0)
        self.labsc_x = Label(self.scoreframe, textvariable=self.score_x, font=('Calibri', 24), fg="cyan", bg="black")
        self.labsc_x.grid(row=0, column=1)

        self.turnframe.rowconfigure(0, weight=1)
        self.turnframe.columnconfigure(0, weight=1)
        self.turnframe.columnconfigure(1, weight=1)
        self.turnframe.grid(row=0, column=2, sticky=EW)

        self.labturn.grid(row=0, column=0, sticky=E)

        self.labturnsym.grid(row=0, column=1, sticky=W)

        self.lab_o = Label(self.scoreframe, text="= O", font=('Calibri', 24, "bold"), fg="red", bg="black")
        self.lab_o.grid(row=0, column=4)
        self.labsc_o = Label(self.scoreframe, textvariable=self.score_o, font=('Calibri', 24), fg="red", bg="black")
        self.labsc_o.grid(row=0, column=3)

        userframe = Frame(self.scoreframe, bg="black", height=30)
        userframe.grid_propagate(False)
        userframe.grid(row=1, column=0, columnspan=5, sticky=EW)
        userframe.columnconfigure(0, weight=1)
        userframe.columnconfigure(1, weight=1)

        self.playerxname.set("Player 1")
        self.playeroname.set("Player 2")
        self.playerx = Label(userframe, textvariable=self.playerxname, bg="black", fg="cyan", font=('Calibri', 18),
                             anchor=NW)
        self.playero = Label(userframe, textvariable=self.playeroname, bg="black", fg="red", font=('Calibri', 18),
                             anchor=NE)
        self.playerx.grid(row=0, column=0, sticky=NSEW)
        self.playero.grid(row=0, column=1, sticky=NSEW)

        # bottom
        boardframe = Frame(self.gamescreen, bg="black")
        boardframe.grid(row=1, column=0, sticky=NSEW)

        buttonframe = Frame(self.gamescreen, bg="black", height=45)
        buttonframe.grid(row=2, column=0, sticky=EW)
        buttonframe.rowconfigure(0, weight=1)
        buttonframe.columnconfigure(0, weight=1)
        buttonframe.columnconfigure(1, weight=1)
        buttonframe.grid_propagate(False)

        self.playagainbutton = Button(buttonframe, text="Play Again", state=DISABLED, activeforeground="green",
                                      activebackground="#242424", disabledforeground="#242424", bg="#353535", fg="lime",
                                      font=('Calibri', 16, "bold"), command=self.play_again)
        self.playagainbutton.grid(row=0, column=0, padx=5, pady=5, sticky=E)
        self.newgamebutton = Button(buttonframe, text="New Game", state=NORMAL, activeforeground="orange4",
                                    activebackground="#242424", disabledforeground="#242424", bg="#353535", fg="orange",
                                    font=('Calibri', 16, "bold"), command=self.new_game)
        self.newgamebutton.grid(row=0, column=1, padx=5, pady=5, sticky=W)

        for i in range(3):
            boardframe.rowconfigure(i, weight=1, uniform="1")
            boardframe.columnconfigure(i, weight=1, uniform="1")

        for i in range(3):
            a = []
            for j in range(3):
                b = Label(boardframe, textvariable=self.board[i][j][1], font=('Calibri', 72), bg="#353535",
                          fg="#696969")
                self.board[i][j][1].set(self.board[i][j][0])
                a.append(b)
                b.grid(row=i, column=j, sticky=NSEW, padx=10, pady=10)
                b.bind("<Button-1>", lambda _, a=(i, j): self.enter_symbol(a))
                self.bind(self.board[i][j][0], lambda _, a=(i, j): self.enter_symbol(a))
            self.board_labels.append(a)

    def start_game(self):
        if self.playerxname.get().strip() == "" or len(self.playerxname.get()) > 20:
            self.playerxname.set("Player 1")
            return
        if self.playeroname.get().strip() == "" or len(self.playeroname.get()) > 20:
            self.playeroname.set("Player 2")
            return

        self.mainscreen.grid_remove()
        self.focus_set()
        self.highlight_turn()

        self.unfreeze()

    def new_game(self, dialog=True):

        def newgame_actions():
            self.reset_board()
            self.score_x.set(0)
            self.score_o.set(0)
            self.matches = 0
            self.current.set('X')
            self.current_color = "cyan"
            self.bind("<Return>", lambda _: [print("", end="")])

            self.mainscreen.grid()

        if dialog and self.matches != 0:
            a = tkinter.messagebox.askyesno("New Game", "Do you really want to start a new game?")
            if not a:
                return

            summary_window = Toplevel()

            winposx = int(self.winfo_x() + (self.winfo_width() - 340) / 2)
            winposy = int(self.winfo_y() + (self.winfo_height() - 330) / 2)
            summary_window.geometry(f"340x330+{winposx}+{winposy}")

            summary_window.title("Game Summary")
            summary_window.focus_set()
            summary_window.grab_set()
            summary_window.update()
            wincol = "#353535"
            summary_window.config(bg=wincol)

            summary_window.resizable(False, False)
            summary_window.bind("<Return>", lambda _: [newgame_actions(), summary_window.destroy()])

            summary_window.columnconfigure(0, weight=1)
            summary_window.columnconfigure(1, weight=1)

            x = self.score_x.get()
            o = self.score_o.get()
            if x > o:
                winner = f'{self.playerxname.get()} WINS'
                winner_color = "cyan"
            elif x < o:
                winner = f'{self.playeroname.get()} WINS'
                winner_color = "red"
            else:
                winner = 'GAME DRAWS'
                winner_color = "white"

            score = f"{x} - {o}" if x > o else f"{o} - {x}"
            matches = self.matches
            draws = self.matches - (o + x)

            Label(summary_window, text="Game Summary", font=("Calibri", 20, "italic"), bg=wincol, fg="yellow"
                  ).grid(row=1, column=0, columnspan=2, padx=20, pady=15, sticky=EW)
            Label(summary_window, text=f"{winner} BY {score}\n",
                  font=("Calibri", 18, "bold", "underline"), bg=wincol, fg=winner_color) \
                .grid(row=2, column=0, columnspan=2, sticky=EW)

            Label(summary_window,
                  text=f"Score: ", font=("Calibri", 16), bg=wincol, fg=self.goldenish
                  ).grid(row=3, column=0, sticky=E)
            Label(summary_window,
                  text=f"{x} - {o} (X - O)", font=("Calibri", 16), bg=wincol, fg="white"
                  ).grid(row=3, column=1, sticky=W)

            Label(summary_window,
                  text=f"Matches: ", font=("Calibri", 16), bg=wincol, fg=self.goldenish
                  ).grid(row=4, column=0, sticky=E)
            Label(summary_window,
                  text=f"{matches}", font=("Calibri", 16), bg=wincol, fg="white"
                  ).grid(row=4, column=1, sticky=W)

            Label(summary_window,
                  text=f"Draws: ", font=("Calibri", 16), bg=wincol, fg=self.goldenish
                  ).grid(row=5, column=0, sticky=E)
            Label(summary_window,
                  text=f"{draws}", font=("Calibri", 16), bg=wincol, fg="white"
                  ).grid(row=5, column=1, sticky=W)

            Button(summary_window, text="CLOSE", font=("Calibri", 16, "bold"), bg=self.goldenish,
                   fg="black", command=lambda: [newgame_actions(), summary_window.destroy()]
                   ).grid(row=6, column=0, columnspan=2, pady=30)

            summary_window.update()

            summary_window.protocol("WM_DELETE_WINDOW", lambda: [newgame_actions(), summary_window.destroy()])
            summary_window.mainloop()
        else:
            newgame_actions()

    def change_curr(self):
        if self.current.get() == "O":
            self.current.set("X")
            self.current_color = "cyan"
        else:
            self.current.set("O")
            self.current_color = "red"

        self.labturnsym.config(fg=self.current_color)

    def reset_board(self):
        for i in range(3):
            for j in range(3):
                self.board_labels[i][j].config(bg="#353535", fg="#696969")
                self.board[i][j][1].set(self.board[i][j][0])
        for child in self.scoreframe.winfo_children() + self.turnframe.winfo_children():
            child.config(bg="black")

        self.moves = ""
        self.clicks = 0
        self.labturn.config(text="Turn")

    def play_again(self):
        self.unfreeze()
        self.playagainbutton.config(state=DISABLED, text="Play Again", command=self.play_again)
        self.newgamebutton.config(state=NORMAL)

        if (self.clicks > 0 and self.clicks % 2 != 0) or self.clicks == 0:
            self.change_curr()

        self.bind("<Return>", lambda _: [print("", end="")])
        self.reset_board()
        self.highlight_turn()
        self.computer_move()

    def enter_symbol(self, x):
        if self.frozen:
            return

        i, j = x
        b = self.board[i][j][1]
        b_index = self.board[i][j][0]
        lab = self.board_labels[i][j]

        if b.get() not in ("X", "O"):
            b.set(self.current.get())
            lab.config(fg=self.current_color)
            self.moves += str(b_index)
            self.clicks += 1

            self.bind("<Return>", lambda _: [print("", end="")])

            win = self.are_ya_winning_son()
            if win:
                self.matches += 1
                self.freeze()
                self.playagainbutton.config(state=NORMAL)
                self.newgamebutton.config(state=NORMAL)
                self.bind("<Return>", lambda _: [self.play_again()])
                self.labturn.config(text="WINNER")
                if win == "X":
                    self.score_x.set(self.score_x.get() + 1)
                else:
                    self.score_o.set(self.score_o.get() + 1)
            else:
                if self.board_is_full():
                    if self.current.get() == "X":
                        b = "O"
                    else:
                        b = "X"
                    self.labturn.config(text=f"DRAW {b}/")
                    self.labturnsym.config(fg="white")
                    self.matches += 1
                    self.freeze()
                    self.playagainbutton.config(state=NORMAL)
                    self.newgamebutton.config(state=NORMAL)
                    self.bind("<Return>", lambda _: [self.play_again()])
                else:
                    self.change_curr()
                    self.highlight_turn()
                    self.computer_move()

    def highlight_turn(self):
        colx = "#0f6b6a"
        colo = "#54092b"
        self.lab_o.config(bg="black")
        self.labsc_o.config(bg="black")
        self.lab_x.config(bg="black")
        self.labsc_o.config(bg="black")

        if self.current.get() == "X":
            self.lab_x.config(bg=colx)
            self.labsc_x.config(bg=colx)
        else:
            self.lab_o.config(bg=colo)
            self.labsc_o.config(bg=colo)

    def computer_move(self):
        if self.opponent.get() == "computer" and self.current.get() == "O":
            self.freeze()
            i, j = self.ai.get_next_move(self.board, self.moves)
            self.after(400, lambda: [self.unfreeze(), self.enter_symbol((i, j))])

    def unfreeze(self):
        self.frozen = False

    def freeze(self):
        self.frozen = True

    def are_ya_winning_son(self):
        win = False
        b = self.board
        bl = self.board_labels
        c = ("X" * 3, "O" * 3)
        win_cols = {"X": "#0f6b6a", "O": "#54092b"}
        col = "black"

        for i in range(3):
            if b[i][0][1].get() + b[i][1][1].get() + b[i][2][1].get() in c:
                win = b[i][0][1].get()
                col = win_cols[win]
                for j in range(3):
                    bl[i][j].config(bg=col)
                break
            elif b[0][i][1].get() + b[1][i][1].get() + b[2][i][1].get() in c:
                win = b[0][i][1].get()
                col = win_cols[win]
                for j in range(3):
                    bl[j][i].config(bg=col)
                break

        if not win and any((
                b[0][0][1].get() + b[1][1][1].get() + b[2][2][1].get() in c,
                b[2][0][1].get() + b[1][1][1].get() + b[0][2][1].get() in c
        )):
            win = b[1][1][1].get()
            col = win_cols[win]
            bl[1][1].config(bg=col)
            if win == b[0][0][1].get() == b[2][2][1].get():
                bl[0][0].config(bg=col)
                bl[2][2].config(bg=col)
            else:
                bl[2][0].config(bg=col)
                bl[0][2].config(bg=col)

        for child in self.scoreframe.winfo_children() + self.turnframe.winfo_children():
            child.config(bg=col)

        return win

    def board_is_full(self):
        return self.clicks == 9

    def start_app(self):
        self.mainloop()


if __name__ == '__main__':
    App()
