from tkinter import *
import tkinter.messagebox
try:
    import AI
except ModuleNotFoundError:
    try:
        from files import AI
    except ModuleNotFoundError:
        exit("AI file not found")


class App(Tk):
    def __init__(self):
        super().__init__()

        self.ai = AI.Bot()

        self.geometry("440x570")
        self.config(bg="black")
        self.title("Tic Tac Toe")
        self.resizable(False, False)
        try:
            self.iconphoto(True, PhotoImage(file="tttlogo.png"))
        except TclError:
            pass

        self.score_x = IntVar()
        self.score_x.set(0)
        self.score_o = IntVar()
        self.score_o.set(0)
        self.current = StringVar()
        self.current.set("X")
        self.current_color = "cyan"

        self.frozen = True
        self.clicks = 0
        self.matches = 0
        self.icons = ("X", "O")
        self.moves = ""

        self.scoreframe = Frame(self, bg="black")
        self.scoreframe.grid(row=0, column=0, sticky=EW)
        self.scoreframe.rowconfigure(0, weight=1)
        self.scoreframe.columnconfigure(2, weight=1)

        self.lab_x = Label(self.scoreframe, text="X =", font=('Calibri', 24, "bold"), fg="cyan", bg="black")
        self.lab_x.grid(row=0, column=0)
        self.labsc_x = Label(self.scoreframe, textvariable=self.score_x, font=('Calibri', 24), fg="cyan", bg="black")
        self.labsc_x.grid(row=0, column=1)

        self.turnframe = Frame(self.scoreframe, bg="black")
        self.turnframe.rowconfigure(0, weight=1)
        self.turnframe.columnconfigure(0, weight=1)
        self.turnframe.columnconfigure(1, weight=1)
        self.turnframe.grid(row=0, column=2, sticky=EW)
        self.labturn = Label(self.turnframe, text="Turn", font=('Calibri', 24), fg="white", bg="black")
        self.labturn.grid(row=0, column=0, sticky=E)
        self.labturnsym = Label(self.turnframe, textvariable=self.current, font=('Calibri', 24), fg="cyan", bg="black")
        self.labturnsym.grid(row=0, column=1, sticky=W)

        self.lab_o = Label(self.scoreframe, text="= O", font=('Calibri', 24, "bold"), fg="red", bg="black")
        self.lab_o.grid(row=0, column=4)
        self.labsc_o = Label(self.scoreframe, textvariable=self.score_o, font=('Calibri', 24), fg="red", bg="black")
        self.labsc_o.grid(row=0, column=3)

        self.userframe = Frame(self.scoreframe, bg="black", height=30)
        self.userframe.grid_propagate(False)
        self.userframe.grid(row=1, column=0, columnspan=5, sticky=EW)
        self.userframe.columnconfigure(0, weight=1)
        self.userframe.columnconfigure(1, weight=1)
        self.playerxname = StringVar()
        self.playeroname = StringVar()
        self.playerxname.set("Player 1")
        self.playeroname.set("Player 2")
        self.playerx = Label(self.userframe, textvariable=self.playerxname, bg="black", fg="cyan", font=('Calibri', 18), anchor=NW)
        self.playero = Label(self.userframe, textvariable=self.playeroname, bg="black", fg="red", font=('Calibri', 18), anchor=NE)
        self.playerx.grid(row=0, column=0, sticky=NSEW)
        self.playero.grid(row=0, column=1, sticky=NSEW)

        self.playerx_entry = Entry(self.userframe, textvariable=self.playerxname, insertbackground="white", bg="#505050", fg="white", font=('Calibri', 18), justify=LEFT)
        self.playero_entry = Entry(self.userframe, textvariable=self.playeroname, insertbackground="white", bg="#505050", fg="white", font=('Calibri', 18), justify=RIGHT)

        # ai vs player
        self.opponent = StringVar()

        def oppo_select():
            if self.opponent.get() == "computer" or self.opponent.get() == "hardbot":
                self.oppo_radio_2p.config(selectcolor="black")
                self.oppo_radio_ai.config(selectcolor="white")
                self.oppo_radio_bot.config(selectcolor="black")
                self.playeroname.set("Computer")

                if self.opponent.get() == "hardbot":
                    self.oppo_radio_ai.config(selectcolor="black")
                    self.oppo_radio_bot.config(selectcolor="white")
                    self.playeroname.set("Hard-Bot")

                self.playero_entry.grid_remove()
                self.playero.grid()
            else:
                self.oppo_radio_2p.config(selectcolor="white")
                self.oppo_radio_ai.config(selectcolor="black")
                self.oppo_radio_bot.config(selectcolor="black")
                self.playeroname.set("Player 2")
                self.playero_entry.grid(row=0, column=1, sticky=NSEW)
                self.playero.grid_remove()

        self.opponent_frame = Frame(self.scoreframe, bg="black")
        self.opponent_frame.grid(row=2, column=0, columnspan=5, sticky=EW, padx=5, pady=5)
        Label(self.opponent_frame, text='Play Against:', bg="black", fg="yellow", font=("Calibri", 14)).grid(row=0, column=0, sticky=W)
        self.oppo_radio_2p = Radiobutton(
            self.opponent_frame,
            text="Player",
            bg="black",
            fg="white",
            font=("Calibri", 14),
            selectcolor="black",
            activebackground="black",
            activeforeground="#aaaaaa",
            variable=self.opponent,
            value="player",
            command=oppo_select
        )
        self.oppo_radio_ai = Radiobutton(
            self.opponent_frame,
            text="Computer",
            bg="black",
            fg="white",
            font=("Calibri", 14),
            selectcolor="black",
            activebackground="black",
            activeforeground="#aaaaaa",
            variable=self.opponent,
            value="computer",
            command=lambda: [oppo_select(), self.ai.normal()]
        )
        self.oppo_radio_bot = Radiobutton(
            self.opponent_frame,
            text="Hard-Bot",
            bg="black",
            fg="white",
            font=("Calibri", 14),
            selectcolor="black",
            activebackground="black",
            activeforeground="#aaaaaa",
            variable=self.opponent,
            value="hardbot",
            command=lambda: [oppo_select(), self.ai.hard()]
        )
        self.oppo_radio_2p.grid(row=0, column=1, sticky=W, padx=5)
        self.oppo_radio_ai.grid(row=0, column=2, sticky=W, padx=5)
        self.oppo_radio_bot.grid(row=0, column=3, sticky=W)
        self.oppo_radio_2p.invoke()

        # bottom
        self.boardframe = Frame(self, bg="black")
        self.boardframe.grid(row=1, column=0, sticky=NSEW)

        self.buttonframe = Frame(self, bg="black", height=45)
        self.buttonframe.grid(row=2, column=0, sticky=EW)
        self.buttonframe.rowconfigure(0, weight=1)
        self.buttonframe.columnconfigure(0, weight=1)
        self.buttonframe.columnconfigure(1, weight=1)
        self.buttonframe.grid_propagate(False)
        self.playagainbutton = Button(self.buttonframe, text="Play Again", state=DISABLED, activeforeground="green", activebackground="#242424", disabledforeground="#242424", bg="#353535", fg="lime", font=('Calibri', 16, "bold"), command=self.play_again)
        self.playagainbutton.grid(row=0, column=0, padx=5, pady=5, sticky=E)
        self.resetbutton = Button(self.buttonframe, text="Reset Scores", state=NORMAL, activeforeground="orange4", activebackground="#242424", disabledforeground="#242424", bg="#353535", fg="orange", font=('Calibri', 16, "bold"), command=self.change_username)
        self.resetbutton.grid(row=0, column=1, padx=5, pady=5, sticky=W)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        for i in range(3):
            self.boardframe.rowconfigure(i, weight=1, uniform="1")
            self.boardframe.columnconfigure(i, weight=1, uniform="1")

        temp = (7, 4, 1)
        self.board = [[[temp[i]+j, StringVar()] for j in range(3)] for i in range(3)]
        self.board_labels = []
        temp = 0
        for i in range(3):
            a = []
            for j in range(3):
                b = Label(self.boardframe, textvariable=self.board[i][j][1], font=('Calibri', 72), bg="#353535", fg="#696969")
                self.board[i][j][1].set(self.board[i][j][0])
                a.append(b)
                b.grid(row=i, column=j, sticky=NSEW, padx=10, pady=10)
                b.bind("<Button-1>", lambda _, a=(i, j): self.enter_symbol(a))
                self.bind(self.board[i][j][0], lambda _, a=(i, j): self.enter_symbol(a))
                temp += 1
            self.board_labels.append(a)

        self.change_username(False)
        self.start()

    def change_username(self, dialog=True):
        if dialog and self.matches != 0:
            a = tkinter.messagebox.askyesno("Reset Scores", "Do you really want to reset the scores?")
            if not a:
                return

            summary = f"GAME DRAWED BY {self.score_x.get()}-{self.score_o.get()}"
            if self.score_x.get() > self.score_o.get():
                summary = f"{self.playerxname.get()} WINS BY {self.score_x.get()}-{self.score_o.get()}"
            elif self.score_x.get() < self.score_o.get():
                summary = f"{self.playeroname.get()} WINS BY {self.score_o.get()}-{self.score_x.get()}"
            output = f"""{30 * '-'}
{summary}

Scores:
    {self.playerxname.get()} (X) = {self.score_x.get()}
    {self.playeroname.get()} (O) = {self.score_o.get()}

Matches Played: {self.matches}
Draws: {self.matches - self.score_x.get() - self.score_o.get()}
{30 * '-'}"""
            tkinter.messagebox.showinfo("Game Summary", output)

        self.clear_board()
        self.score_x.set(0)
        self.score_o.set(0)
        self.matches = 0
        self.current.set('')
        self.freeze()
        self.playagainbutton.config(state=NORMAL, text="Start Game", command=lambda a=True: self.play_again(a))
        self.resetbutton.config(state=DISABLED)

        self.oppo_radio_ai.config(state=NORMAL)
        self.oppo_radio_2p.config(state=NORMAL)
        self.oppo_radio_bot.config(state=NORMAL)

        self.labturn.config(text="Choose Names")
        self.playerx.grid_remove()

        if self.opponent.get() not in ("computer", "hardbot"):
            self.playero.grid_remove()
            self.playero_entry.grid(row=0, column=1, sticky=NSEW, padx=4)

        self.playerx_entry.grid(row=0, column=0, sticky=NSEW, padx=4)
        self.playerx_entry.focus_set()
        self.playerx_entry.selection_range(0, END)

    def change_curr(self):
        if self.current.get() == "X":
            self.current.set("O")
            self.current_color = "red"
        elif self.current.get() == "O":
            self.current.set("X")
            self.current_color = "cyan"
        else:
            self.current.set("X")
            self.current_color = "cyan"
        self.labturnsym.config(fg=self.current_color)

    def clear_board(self):
        temp = 0
        self.focus_set()
        for i in range(3):
            for j in range(3):
                self.board[i][j][1].set("")
                self.board_labels[i][j].config(bg="#353535", fg="#696969")
                self.board[i][j][1].set(self.board[i][j][0])
                temp += 1
        for child in self.scoreframe.winfo_children() + self.turnframe.winfo_children():
            child.config(bg="black")

    def play_again(self, validate_names=False):
        names_valid = True
        if validate_names:
            if len(self.playerxname.get()) > 12 or len(self.playeroname.get()) > 12:
                tkinter.messagebox.showerror("Invalid Username", "Username must be less than 12 characters")
                names_valid = False

                if len(self.playerxname.get()) > 12:
                    self.playerx_entry.focus_set()
                    self.playerxname.set("")
                elif len(self.playeroname.get()) > 12:
                    self.playero_entry.focus_set()
                    self.playeroname.set("")

            elif self.playerxname.get().strip() == '':
                self.playerxname.set("Player 1")
            elif self.playeroname.get().strip() == '':
                self.playeroname.set("Player 2")

        if not names_valid:
            return

        self.playerx.grid()
        self.playero.grid()
        self.clear_board()
        self.unfreeze()
        self.playagainbutton.config(state=DISABLED, text="Play Again", command=self.play_again)
        self.resetbutton.config(state=NORMAL)

        self.oppo_radio_2p.config(state=DISABLED)
        self.oppo_radio_ai.config(state=DISABLED)
        self.oppo_radio_bot.config(state=DISABLED)

        self.bind("<Return>", lambda _: [print()])
        self.labturn.config(text="Turn")
        self.playerx_entry.grid_forget()
        self.playero_entry.grid_forget()

        if (self.clicks > 0 and self.clicks % 2 != 0) or self.clicks == 0:
            self.change_curr()

        self.clicks = 0
        self.moves = ""

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
            self.resetbutton.config(state=DISABLED)
            win = self.are_ya_winning_son()
            if win:
                self.matches += 1
                self.freeze()
                self.playagainbutton.config(state=NORMAL)
                self.resetbutton.config(state=NORMAL)
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
                    self.resetbutton.config(state=NORMAL)
                    self.bind("<Return>", lambda _: [self.play_again()])
                else:
                    self.change_curr()
                    self.computer_move()

    def computer_move(self):
        if self.opponent.get() in ("computer", "hardbot") and self.current.get() == "O":
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
        self.opponent_frame.config(bg="black")

        return win

    def board_is_full(self):
        return self.clicks == 9

    def start(self):
        self.mainloop()


if __name__ == '__main__':
    App()
