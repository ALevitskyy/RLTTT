import math
import numpy as np
from minmax_agent import minmaxagent

# from winning_combos import check_gamestate
class tictactoe:
    def __init__(self, dimension, dimension2, order):
        # dimension- length #dimensionw-width, order - how many x`s in a row
        if order > dimension and order > dimension2:
            raise tictactoe.orderError
        else:
            self.dimension = dimension
            self.dimension2 = dimension2
            self.order = order
            self.board = np.zeros((dimension, dimension2), dtype=str)
            self.sequence_x = []
            self.sequence_o = []
            self.gamestate = "in_play"
            self.whose_move = "X"

    def eligble_point(self, move_code):
        if move_code[0] < self.dimension and move_code[0] >= 0:
            if move_code[1] < self.dimension2 and move_code[1] >= 0:
                return True
        return False

    def check_gamestate(self, move_code, whose_move):
        down_diagonal = [
            [move_code[0] + i, move_code[1] + i]
            for i in range(-self.order + 1, self.order)
            if self.eligble_point([move_code[0] + i, move_code[1] + i])
        ]
        up_diagonal = [
            [move_code[0] - i, move_code[1] + i]
            for i in range(-self.order + 1, self.order)
            if self.eligble_point([move_code[0] - i, move_code[1] + i])
        ]
        vertical = [
            [move_code[0] + i, move_code[1]]
            for i in range(-self.order + 1, self.order)
            if self.eligble_point([move_code[0] + i, move_code[1]])
        ]
        horizontal = [
            [move_code[0], move_code[1] + i]
            for i in range(-self.order + 1, self.order)
            if self.eligble_point([move_code[0], move_code[1] + i])
        ]
        down_diagonal = [
            down_diagonal[i : (i + self.order)]
            for i in range(0, len(down_diagonal) - self.order + 1)
        ]
        up_diagonal = [
            up_diagonal[i : (i + self.order)]
            for i in range(0, len(up_diagonal) - self.order + 1)
        ]
        vertical = [
            vertical[i : (i + self.order)]
            for i in range(0, len(vertical) - self.order + 1)
        ]
        horizontal = [
            horizontal[i : (i + self.order)]
            for i in range(0, len(horizontal) - self.order + 1)
        ]
        if whose_move == "X":
            for elem3 in down_diagonal:
                if all(elem in self.sequence_x for elem in elem3):
                    return "win_x"
            for elem3 in up_diagonal:
                if all(elem in self.sequence_x for elem in elem3):
                    return "win_x"
            for elem3 in vertical:
                if all(elem in self.sequence_x for elem in elem3):
                    return "win_x"
            for elem3 in horizontal:
                if all(elem in self.sequence_x for elem in elem3):
                    return "win_x"
        else:
            for elem3 in down_diagonal:
                if all(elem in self.sequence_o for elem in elem3):
                    return "win_o"
            for elem3 in up_diagonal:
                if all(elem in self.sequence_o for elem in elem3):
                    return "win_o"
            for elem3 in vertical:
                if all(elem in self.sequence_o for elem in elem3):
                    return "win_o"
            for elem3 in horizontal:
                if all(elem in self.sequence_o for elem in elem3):
                    return "win_o"
        if (
            len(self.sequence_o) + len(self.sequence_x)
            == self.dimension * self.dimension2
        ):
            return "draw"
        return "in_play"

    def moves_generator(self):
        output = []
        for i in range(self.dimension):
            for j in range(self.dimension2):
                if self.board[i, j] == "":
                    output.append([i, j])
        return output

    def make_move(self, move_code):
        if move_code not in self.moves_generator():
            raise tictactoe.ineligibleMove
        if self.gamestate != "in_play":
            raise tictactoe.gameover
        else:
            if (len(self.sequence_x) + len(self.sequence_o)) % 2 == 0:
                self.whose_move = "X"
                self.sequence_x.append(move_code)
                self.board[move_code[0], move_code[1]] = "X"
                # print("Next Move O")
            else:
                self.whose_move = "O"
                self.sequence_o.append(move_code)
                self.board[move_code[0], move_code[1]] = "O"
                # print("Next Move X")
        # self.print_board()
        self.gamestate = self.check_gamestate(move_code, self.whose_move)
        if self.gamestate == "in_play":
            if self.whose_move == "O":
                self.whose_move = "X"
            else:
                self.whose_move = "O"
        # print(self.sequence_x)
        # print(self.sequence_x)
        # print(self.gamestate)
        pass

    def print_board(self):
        print(self.board)
        pass

    class orderError(Exception):
        def __init__(self):
            self.text = "Order>Dimension"

        def __str__(self):
            return self.text

    class ineligibleMove(Exception):
        def __init__(self):
            self.text = "ineligibleMove"

        def __str__(self):
            return self.text

    class gameover(Exception):
        def __init__(self):
            self.text = "gameover"

        def __str__(self):
            return self.text


test = tictactoe(3, 3, 3)
test.make_move([1, 1])
