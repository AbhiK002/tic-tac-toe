import random


class Bot:
    def __init__(self):
        self.computer = "O"
        self.mode = "normal"  # or "hard"
        self.indexed_board = {
            7: (0, 0), 8: (0, 1), 9: (0, 2),
            4: (1, 0), 5: (1, 1), 6: (1, 2),
            1: (2, 0), 2: (2, 1), 3: (2, 2)
        }

        self.nums = set(range(1, 10))
        self.empty_spaces = set()

        self.high_priority = {1, 3, 7, 9}

        # DEFENSE
        self.move4HIGH = {  # rev
            "159.753": (2, 4, 6, 8),
            "156.952": 3, "756.358": 9,
            "158.954": 7, "752.354": 1
        }
        self.move4MED = {  # rev
            "258.456": (1, 3, 7, 9),
            "254": 1, "256": 3, "658": 9, "458": 7
        }
        self.move4LOW = {
            "519.591": (3, 7),
            "573.537": (1, 9)
        }

        # ATTACK
        self.move3HIGH = {
            "15.13,17.32,38,74,76": 9,
            "95.97,93.36,34,78,72,73,37": 1,
            "35.31,39.12,18,96,94": 7,
            "75.79,71.14,16,19,91,98,92": 3
        }
        self.move5HIGH = {  # rev
            "127.143.371.731": 9, "329.361.193.913": 7,
            "967.983": 1, "749.781": 3
        }

        self.med_priority = {2, 4, 6, 8}
        self.low_priority = {5}

        self.win_criteria = (
            {7, 8, 9}, {4, 5, 6}, {1, 2, 3},  # horizontal
            {7, 4, 1}, {8, 5, 2}, {9, 6, 3},  # vertical
            {7, 5, 3}, {9, 5, 1}  # diagonal
        )


    def hard(self):
        self.mode = "hard"

    def normal(self):
        self.mode = "normal"

    def get_next_move(self, board, now):
        win_index = None

        set_now = set(map(int, now))
        self.empty_spaces = self.nums - set_now
        for crit in self.win_criteria:
            remaining = crit - set_now
            contains = list(crit & set_now)
            if len(remaining) == 1 and (
                self.get_sym(contains[0], board) == self.get_sym(contains[1], board)
            ):
                i = remaining.pop()
                if self.get_sym(i, board) not in "XO":
                    if self.get_sym(contains[0], board) == self.computer:
                        return self.indexed_board[i]
                    win_index = i

        if win_index is not None:
            return self.indexed_board[win_index]
        else:
            if self.mode == "normal":
                return self.indexed_board[random.choice(list(self.empty_spaces))]
            elif self.mode == "hard":
                if len(now) == 0:
                    return self.indexed_board[random.choice(list(self.high_priority))]

                elif len(now) == 1:
                    if int(now[0]) in self.high_priority or int(now[0]) in self.med_priority:
                        return self.indexed_board[5]
                    else:
                        return self.indexed_board[random.choice(list(self.high_priority))]

                elif len(now) == 2:
                    move3 = None
                    search_dict = None

                    if int(now[0]) in self.high_priority:
                        search_dict = self.move3HIGH
                    elif int(now[0]) in self.low_priority:
                        search_dict = None

                    for i, j in search_dict.items():
                        if now in i:
                            move3 = j
                            break

                    if move3 is None:
                        return self.indexed_board[random.choice(list(self.empty_spaces))]
                    else:
                        return self.indexed_board[move3]

                elif len(now) == 3:
                    move4 = None

                    if int(now[0]) in self.high_priority:
                        search_dict = self.move4HIGH
                    elif int(now[0]) in self.med_priority:
                        search_dict = self.move4MED
                    else:
                        search_dict = self.move4LOW

                    for i, j in search_dict.items():
                        if now in i or (search_dict != self.move4LOW and now in i[::-1]):
                            move4 = j
                            break

                    if type(move4) is tuple:
                        move4 = random.choice(move4)
                    elif move4 is None:
                        move4 = random.choice(list(self.empty_spaces))

                    return self.indexed_board[move4]

                elif len(now) == 4:
                    move5 = None
                    search_dict = None

                    if int(now[0]) in self.high_priority:
                        search_dict = self.move5HIGH
                    elif int(now[0]) in self.low_priority:
                        search_dict = None

                    for i, j in search_dict.items():
                        if now[:3] in i or now[:3] in i[::-1]:
                            move5 = j
                            break

                    if move5 is None:
                        return self.indexed_board[random.choice(list(self.empty_spaces))]
                    else:
                        return self.indexed_board[move5]

                else:
                    return self.indexed_board[random.choice(list(self.empty_spaces))]

    def get_sym(self, ind, given_board):
        i, j = self.indexed_board[ind]
        return given_board[i][j][1].get()
