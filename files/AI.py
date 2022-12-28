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
        self.med_priority = {2, 4, 6, 8}
        self.low_priority = {5}

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
        self.move3HIGHLOW = {
            "15.13,17.51": [9],
            "95.97,93.59": [1],
            "35.31,39.53": [7],
            "75.79,71.57": [3],

            "12.54": [7, 9], "32": [9, 7],
            "14": [3, 9], "74.58": [9, 3],
            "36.52": [1, 7], "96": [7, 1],
            "98.56": [3, 1], "78": [1, 3],

            "38.76": [9, 1], "18.94": [7, 3],
            "37.73.34.72": [1, 9], "19.91.16.92": [3, 7],

        }
        self.move5LOW = {
            "5198.5914": 3,
            "5196.5912": 7,
            "5374.5732": 9,
            "5378.5736": 1
        }

        self.win_criteria = (
            {7, 8, 9}, {4, 5, 6}, {1, 2, 3},  # horizontal
            {7, 4, 1}, {8, 5, 2}, {9, 6, 3},  # vertical
            {7, 5, 3}, {9, 5, 1}  # diagonal
        )

        self.next_moves = []  # next moves of computer

    def hard(self):
        self.mode = "hard"

    def normal(self):
        self.mode = "normal"

    def easy(self):
        self.mode = "easy"

    def get_next_move(self, board, now):
        print(f"computer got: '{now}'")
        win_index = None
        set_now = set(map(int, now))
        self.empty_spaces = self.nums - set_now

        if self.mode == "easy":
            self.next_moves.clear()
            return self.indexed_board[random.choice(list(self.empty_spaces))]

        for crit in self.win_criteria:
            remaining = list(crit - set_now)
            contains = list(crit & set_now)
            if len(remaining) == 1 and (
                self.get_sym(contains[0], board) == self.get_sym(contains[1], board)
            ):
                i = remaining[0]
                if self.get_sym(i, board) not in "XO":
                    if self.get_sym(contains[0], board) == self.computer:
                        win_index = i
                        break
                    win_index = i

        if win_index is not None:
            self.next_moves.clear()
            return self.indexed_board[win_index]
        else:
            if self.mode == "normal":
                return self.indexed_board[random.choice(list(self.empty_spaces))]
            elif self.mode == "hard":

                # check if there is a specific move to be done
                if self.next_moves:
                    return self.indexed_board[self.next_moves.pop()]

                # if there is no specific move defined, check and make them

                else:
                    if len(now) == 0:  # computer first move
                        sample_space = list(self.low_priority) + [random.choice(list(self.high_priority))]
                        self.next_moves.append(random.choice(sample_space))

                    elif len(now) == 1:  # player first move, computer's second move
                        if int(now[0]) in self.high_priority or int(now[0]) in self.med_priority:
                            self.next_moves.append(5)
                        else:
                            self.next_moves.append(random.choice(list(self.high_priority)))

                    elif len(now) == 2:  # computer first move, computer's third move
                        move3 = None
                        search_dict = self.move3HIGHLOW

                        for i, j in search_dict.items():
                            if now in i:
                                move3 = j
                                break

                        if move3 is None:
                            self.next_moves.append(self.indexed_board[random.choice(list(self.empty_spaces))])
                        else:
                            self.next_moves.extend(move3[::-1])

                    elif len(now) == 3:  # player first move, computer's fourth move
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

                        self.next_moves.append(move4)

                    elif len(now) == 4:
                        move5 = None
                        search_dict = self.move5LOW

                        for i, j in search_dict.items():
                            if now in i:
                                move5 = j
                                break

                        if move5 is None:
                            self.next_moves.append(self.indexed_board[random.choice(list(self.empty_spaces))])
                        else:
                            self.next_moves.append(move5)

                    else:
                        self.next_moves.append(random.choice(list(self.empty_spaces)))

                return self.indexed_board[self.next_moves.pop()]

            else:  # just in case, although highly unlikely
                return self.indexed_board[random.choice(list(self.empty_spaces))]

    def get_sym(self, ind, given_board):
        i, j = self.indexed_board[ind]
        return given_board[i][j][1].get()