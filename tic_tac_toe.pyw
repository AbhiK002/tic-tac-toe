from tkinter import *


class App(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("400x500")
        self.config(bg="black")
        self.title("Tic Tac Toe")
        self.resizable(False, False)
        
        self.score_x = IntVar()
        self.score_x.set(0)
        self.score_o = IntVar()
        self.score_o.set(0)
        self.current = StringVar()
        self.current.set("X")
        self.current_color = "cyan"

        self.frozen = False
        self.clicks = 0

        self.scoreframe = Frame(self, bg="yellow")
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
        
        
        self.boardframe = Frame(self, bg="black")
        self.boardframe.grid(row=1, column=0, sticky=NSEW)
        
        self.buttonframe = Frame(self, bg="black", height=50)
        self.buttonframe.grid(row=2, column=0, sticky=EW)
        self.buttonframe.rowconfigure(0, weight=1)
        self.buttonframe.grid_propagate(False)
        self.playagainbutton = Button(self.buttonframe, text="Play Again", state=DISABLED, disabledforeground="#242424", bg="#353535", fg="lime", font=('Calibri', 16, "bold"), command=self.clear_board)
        self.playagainbutton.grid(row=0, column=0, sticky=NS, padx=10, pady=2)
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        for i in range(3):
            self.boardframe.rowconfigure(i, weight=1, uniform="1")
            self.boardframe.columnconfigure(i, weight=1, uniform="1")

        self.board = [[StringVar() for _ in range(3)] for _ in range(3)]
        self.board_labels = []
        temp = 0
        nums = ['7', '8', '9', '4', '5', '6', '1', '2', '3']
        for i in range(3):
            a = []
            for j in range(3):
                b = Label(self.boardframe, textvariable=self.board[i][j], font=('Calibri', 72), bg="#353535")
                a.append(b)
                b.grid(row=i, column=j, sticky=NSEW, padx=10, pady=10)
                b.bind("<Button-1>", lambda _, a = self.board[i][j], c = b: self.enter_symbol(a, c))
                self.bind(nums[temp], lambda _, a = self.board[i][j], c = b: self.enter_symbol(a, c))
                temp += 1
            self.board_labels.append(a)
            
        self.start()
    
    def change_curr(self):
        if self.current.get() == "X":
            self.current.set("O")
            self.current_color = "red"
            self.labturnsym.config(fg=self.current_color)
        else:
            self.current.set("X")
            self.current_color = "cyan"
            self.labturnsym.config(fg=self.current_color)

    def clear_board(self):
        for i in range(3):
            for j in range(3):
                self.board[i][j].set("")
                self.board_labels[i][j].config(bg="#353535")
        self.frozen = False
        self.playagainbutton.config(state=DISABLED)
        self.bind("<Return>", lambda _: [print()])
        self.clicks = 0
        self.change_curr()
        self.labturn.config(text="Turn")

    def enter_symbol(self, b, lab):
        if self.frozen:
            return
        
        if b.get() not in ("X", "O"):
            b.set(self.current.get())
            lab.config(fg=self.current_color)
            self.clicks += 1
            win = self.are_ya_winning_son()
            if win:
                self.frozen = True
                self.playagainbutton.config(state=NORMAL)
                self.bind("<Return>", lambda _: [self.clear_board()])
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
                    self.frozen = True
                    self.playagainbutton.config(state=NORMAL)
                    self.bind("<Return>", lambda _: [self.clear_board()])
                else:
                    self.change_curr()

    def are_ya_winning_son(self):
        yes = True
        nope = False
        b = self.board
        bl = self.board_labels
        c = ("X"*3, "O"*3)
        win_cols = {"X": "#0f6b6a", "O": "#54092b"}

        for i in range(3):
            if b[i][0].get() + b[i][1].get() + b[i][2].get() in c:
                yes = b[i][0].get()
                col = win_cols[yes]
                bl[i][0].config(bg=col)
                bl[i][1].config(bg=col)
                bl[i][2].config(bg=col)
                return yes
            elif b[0][i].get() + b[1][i].get() + b[2][i].get() in c:
                yes = b[0][i].get()
                col = win_cols[yes]
                bl[0][i].config(bg=col)
                bl[1][i].config(bg=col)
                bl[2][i].config(bg=col)
                return yes
            
        if any((
            b[0][0].get() + b[1][1].get() + b[2][2].get() in c,
            b[2][0].get() + b[1][1].get() + b[0][2].get() in c
            )):
            yes = b[1][1].get()
            col = win_cols[yes]
            bl[1][1].config(bg=col)
            if yes == b[0][0].get() == b[2][2].get():
                bl[0][0].config(bg=col)
                bl[2][2].config(bg=col)
            else:
                bl[2][0].config(bg=col)
                bl[0][2].config(bg=col)
            return yes
        
        return nope

    def board_is_full(self):
        return self.clicks == 9
    
    def start(self):
        self.mainloop()


if __name__ == '__main__':
    App()
