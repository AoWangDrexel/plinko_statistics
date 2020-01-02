import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import random

plt.style.use("seaborn-whitegrid")


"""A Plinko Simulation

"""


def get_board():
    """
    
    """
    SLOTS = [chr(65 + i) for i in range(9)]
    MONEY = [letter.lower() for letter in SLOTS.copy()]
    for i in range(len(SLOTS) * 2 - 1):
        if i % 2 != 0:
            SLOTS.insert(i, "o")
            MONEY.insert(i, "|")
    BOARD = [" " if i % 2 != 0 else "o" for i in range(12 * 17)]
    BOARD = np.array(BOARD).reshape(12, 17)
    BOARD = np.vstack((SLOTS, BOARD))
    BOARD = np.vstack((BOARD, MONEY))
    return BOARD


class PlinkoPuck:
    """
    
    
    """

    BOARD = get_board()

    def __init__(self, letter=None, mark=None):
        self.letter = letter
        self.mark = mark
        if self.letter == None:
            self.letter = "E"
        if self.mark == None:
            self.mark = "P"

    def __check_boundary(self, y):
        if y < 0:
            y = 1
        if y > len(self.BOARD[0]) - 1:
            y = 15
        return y

    def set_letter(self, letter):
        self.letter = letter

    def get_letter(self):
        return self.letter

    def set_mark(self, mark):
        self.mark = mark

    def get_mark(self):
        return self.mark

    def run_simulation(self, show=False):
        slot = np.where(self.BOARD == self.get_letter())
        i, x, y = 1, slot[0] + 1, slot[1]
        self.BOARD[x, y] = self.mark
        for turn in range(12):
            if random.randint(0, 1) == 0:
                x += 1
                y -= 1
            else:
                x += 1
                y += 1
            y = self.__check_boundary(y)
            self.BOARD[x, y] = self.mark
            if x == 13:
                if show:
                    print(self.BOARD)
                return x, y
        return -1


def show_bar(letter, number_of_pucks):
    plinko = PlinkoPuck(letter)
    money_dict = {chr(ord("a") + i): 0 for i in range(9)}
    for i in range(number_of_pucks):
        money_dict["".join(get_board()[plinko.run_simulation()])] += 1
    plt.bar(money_dict.keys(), money_dict.values())
    plt.title(letter)
    plt.show()


def show_all_bars(number_of_pucks):
    plinkos = [PlinkoPuck(chr(65 + i)) for i in range(9)]
    fig, axs = plt.subplots(3, 3)
    list_of_dicts, idx = [], 0
    for i in range(9):
        money_dict = {chr(ord("a") + i): 0 for i in range(9)}
        for j in range(number_of_pucks):
            money_dict["".join(get_board()[plinkos[i].run_simulation()])] += 1
        list_of_dicts.append(money_dict)
    for i in range(3):
        for j in range(3):
            axs[i, j].bar(list_of_dicts[idx].keys(), list_of_dicts[idx].values())
            axs[i, j].set_title(chr(ord("A") + idx))
            idx += 1
    plt.show()


def main():
    plinko = PlinkoPuck("A")
    money_dict = {chr(ord("a") + i): 0 for i in range(9)}
    for i in range(1000):
        money_dict["".join(get_board()[plinko.run_simulation()])] += 1
    print(pd.Series(money_dict))

if __name__ == "__main__":
    main()