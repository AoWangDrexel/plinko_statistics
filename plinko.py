import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random


def get_board():
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


def check_boundary(y):
    if y < 0:
        y = 1
    if y > len(BOARD[0]) - 1:
        y = 15
    return y


BOARD = get_board()


def run_simulation(letter):
    slot = np.where(BOARD == letter)
    i, x, y = 1, slot[0] + 1, slot[1]
    BOARD[x, y] = "P"
    for turn in range(12):
        if random.randint(0, 1) == 0:
            x += 1
            y -= 1
            y = check_boundary(y)
        else:
            x += 1
            y += 1
            y = check_boundary(y)
        BOARD[x, y] = "P"
        if x == 13:
            # print(BOARD)
            return (x, y)
    return -1


def main():
    money_dict = {str([chr(ord("a") + i)]): 0 for i in range(9)}
    for i in range(100000):
        money_dict[str(get_board()[run_simulation("A")])] += 1
    for i in money_dict:
        print(i + str(money_dict[i] / 100000))


if __name__ == "__main__":
    main()