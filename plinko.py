import numpy as np
import matplotlib.pyplot as plt
import random

plt.style.use("seaborn-whitegrid")


"""A Plinko Simulation

The module provides a text-based simulation of thePlinko game from
the game show, The Price is Right. In addition to the simulation, there
are methods that effectively show the outcomes of releasing the puck from
one of the slots to the outcomes of all of the slots. The module can aid
in the crucial question of "What is the best slot for me to win the $10,000?"
Well you are in luck!
"""


def get_board():
    """Creates the Plinko board.
    
    Args:
        None
    
    Returns:
        numpy.ndarray: The Plinko board.
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
    """A class representing the Plinko puck.
    
    Attributes
    ==========
        BOARD (numpy.ndarray): The Plinko board.
    """

    BOARD = get_board()

    def __init__(self, letter=None, mark=None):
        """Initializes PlinkoPuck object's slot letter and mark.
        
        Note
        ====
        The default initialization is dropped at E and marked with P.
        
        Args:
            letter (str): A letter that shows where the puck dropped.
            mark (str): A mark signfying the path the puck followed.
        """
        self.letter = letter
        self.mark = mark
        if self.letter == None:
            self.letter = "E"
        if self.mark == None:
            self.mark = "P"

    def __check_boundary(self, y):
        """Checks the left-most and right-most boundaries.
        
        Args:
            y (int): A y-coordinate.
        
        Returns:
            int: A y-coordinate that does not go through the boundaries.
        """
        if y < 0:
            y = 1
        if y > len(self.BOARD[0]) - 1:
            y = 15
        return y
    
    def set_letter(self, letter):
        self.letter = letter
    
    def get_letter(self):
        """str: A letter slot.
        """
        return self.letter
    
    def set_mark(self, mark):
        self.mark = mark
    
    def get_mark(self):
        """str: A mark to show the path of the puck.
        """
        return self.mark

    def run_simulation(self, show=False):
        """Runs the simulation of the Plinko game.
        
        Args:
            show (bool): If true the method will display the path of the puck.
        
        Returns:
            tuple: The x,y coordinate of which money slot the puck dropped.
        """
        BOARD1 = get_board()
        slot = np.where(BOARD1 == self.get_letter())
        i, x, y = 1, slot[0] + 1, slot[1]
        BOARD1[x, y] = self.mark
        for turn in range(12):
            if random.randint(0, 1) == 0:
                x += 1
                y -= 1
            else:
                x += 1
                y += 1
            y = self.__check_boundary(y)
            BOARD1[x, y] = self.mark
            if x == 13:
                if show:
                    print(BOARD1)
                return x, y
        return -1


def show_bar(letter, number_of_pucks):
    """Creates a bar graph of the chosen letter slot and counting the number of pucks
       in each money slot.
    
    Args:
        letter (str): The letter slot.
        number_of_pucks (int): The number of trials.
    
    Returns:
        None
    """
    plinko = PlinkoPuck(letter)
    money_dict = {chr(ord("a") + i): 0 for i in range(9)}
    for i in range(number_of_pucks):
        money_dict["".join(get_board()[plinko.run_simulation()])] += 1
    plt.bar(money_dict.keys(), [value/number_of_pucks for value in money_dict.values()])
    plt.title(letter)
    plt.show()


def show_all_bars(number_of_pucks):
    """Creates bar graphs of all the letter slots and counting the number of pucks
       in each money slot.
    
    Args:
        number_of_pucks (int): The number of trials.
    
    Returns:
        None
    """
    plinkos = [PlinkoPuck(chr(65 + i)) for i in range(9)]
    fig, axs = plt.subplots(3, 3, figsize=(25,15))
    list_of_dicts, idx = [], 0
    for i in range(9):
        money_dict = {chr(ord("a") + i): 0 for i in range(9)}
        for j in range(number_of_pucks):
            money_dict["".join(get_board()[plinkos[i].run_simulation()])] += 1
        list_of_dicts.append(money_dict)
    for i in range(3):
        for j in range(3):
            axs[i, j].bar(list_of_dicts[idx].keys(), [value/number_of_pucks for value in list_of_dicts[idx].values()])
            axs[i, j].set_title(chr(ord("A") + idx))
            idx += 1
    plt.show()


def main():
    print("View the Jupyer Notebook to learn more about the simulation and the statistics of Plinko.")
    plinko = PlinkoPuck()
    plinko.run_simulation(True)

if __name__ == "__main__":
    main()