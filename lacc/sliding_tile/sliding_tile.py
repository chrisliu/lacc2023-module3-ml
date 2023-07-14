import heapq
import random
from time import sleep

import numpy as np
from IPython.display import clear_output, display, HTML


class SlidingRow:
    def __init__(self, start, size, longest_number):
        self.puzzle = [i for i in range(start, start + size)]
        self.longest_number = longest_number

    def __getitem__(self, key):
        return self.puzzle[key]

    def __setitem__(self, key, value):
        self.puzzle[key] = value

    def __len__(self):
        return len(self.puzzle)

    def __str__(self):
        print_string = "| "
        for i in self.puzzle:
            if i == 0:
                print_string += " " * self.longest_number
            else:
                print_string += str(i) + " " * (self.longest_number - len(str(i)))
            print_string += " " * (self.longest_number)
        print_string += "|\n"
        return print_string

    def to_array(self):
        return self.puzzle


class SlidingTile:
    def __init__(self, size, puzzle=None):
        longest_number = len(str(size * size))

        self.puzzle = [SlidingRow(i * size, size, longest_number) for i in range(size)]

        if puzzle is not None:
            for i in range(size):
                for j in range(size):
                    self.puzzle[i][j] = puzzle[i][j]

    def blank_tile(self):
        for i in range(len(self.puzzle)):
            for j in range(len(self.puzzle)):
                if self.puzzle[i][j] == 0:
                    return (i, j)

    def __len__(self):
        return len(self.puzzle)

    def __eq__(self, other):
        for i in range(len(self.puzzle)):
            for j in range(len(self.puzzle)):
                if self.puzzle[i][j] != other[i][j]:
                    return False
        return True

    @property
    def shape(self):
        return (len(self.puzzle), len(self.puzzle[0]))

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.puzzle[key]
        elif isinstance(key, tuple):
            return self.puzzle[key[0]][key[1]]
        else:
            raise TypeError("Invalid key type", key)

    def __setitem__(self, key, value):
        if isinstance(key, int):
            self.puzzle[key] = value
        elif isinstance(key, tuple):
            self.puzzle[key[0]][key[1]] = value
        else:
            raise TypeError("Invalid key type", key)

    def __str__(self) -> str:
        print_string = "-" * (len(str(self.puzzle[0])) - 1) + "\n"
        for row in self.puzzle:
            print_string += str(row)
        print_string += "-" * (len(str(self.puzzle[0])) - 1)
        return print_string

    def copy(self):
        return SlidingTile(len(self.puzzle), self.puzzle)

    def to_array(self):
        return [row.to_array() for row in self.puzzle]

    def print_actions(self, actions, time_per_action=1):
        def slide_up(puzzle):
            x_blank_tile, y_blank_tile = puzzle.blank_tile()
            if x_blank_tile == 0:
                raise ValueError("Cannot slide up", puzzle)
            puzzle[x_blank_tile][y_blank_tile] = puzzle[x_blank_tile - 1][y_blank_tile]
            puzzle[x_blank_tile - 1][y_blank_tile] = 0

        def slide_down(puzzle):
            x_blank_tile, y_blank_tile = puzzle.blank_tile()
            if x_blank_tile == puzzle.shape[1] - 1:
                raise ValueError("Cannot slide down", puzzle)
            puzzle[x_blank_tile][y_blank_tile] = puzzle[x_blank_tile + 1][y_blank_tile]
            puzzle[x_blank_tile + 1][y_blank_tile] = 0

        def slide_left(puzzle):
            x_blank_tile, y_blank_tile = puzzle.blank_tile()
            if y_blank_tile == 0:
                raise ValueError("Can't slide left", puzzle)
            puzzle[x_blank_tile][y_blank_tile] = puzzle[x_blank_tile][y_blank_tile - 1]
            puzzle[x_blank_tile][y_blank_tile - 1] = 0

        def slide_right(puzzle):
            x_blank_tile, y_blank_tile = puzzle.blank_tile()
            if y_blank_tile == puzzle.shape[0] - 1:
                raise ValueError("Cannot slide right", puzzle)
            puzzle[x_blank_tile][y_blank_tile] = puzzle[x_blank_tile][y_blank_tile + 1]
            puzzle[x_blank_tile][y_blank_tile + 1] = 0

        actions_dict = {
            "u": slide_up,
            "U": slide_up,
            "up": slide_up,
            "d": slide_down,
            "D": slide_down,
            "down": slide_down,
            "l": slide_left,
            "L": slide_left,
            "left": slide_left,
            "r": slide_right,
            "R": slide_right,
            "right": slide_right,
        }

        def print_puzzle(puzzle):
            if is_notebook():
                dh.update(str(puzzle))
            else:
                print("\033[F" * 5, end="")
                print(puzzle)

        puzzle = self.copy()  # don't want to modify the original puzzle
        if is_notebook():
            dh = display(str(puzzle), display_id=True)
        else:
            print(puzzle)

        for action in actions:
            sleep(time_per_action)
            actions_dict[action](puzzle)
            print_puzzle(puzzle)


def is_notebook() -> bool:
    try:
        shell = get_ipython().__class__.__name__
        if shell == "ZMQInteractiveShell":
            return True  # Jupyter notebook or qtconsole
        elif shell == "TerminalInteractiveShell":
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False  # Probably standard Python interpreter


def goal_state(n):
    goal = list(range(1, n * n))
    goal.append(0)
    goal = np.array(goal).reshape(n, n)
    return SlidingTile(n, goal)


def middle_state(n):
    state = list(range(1, n * n))
    state.insert(int(n * n / 2), 0)
    state = np.array(state).reshape(n, n)
    return SlidingTile(n, state)


def generate_valid_sliding_tile(n):
    """Generates a valid sliding tile puzzle given the size of the puzzle
    n: the number of rows and columns in the puzzle
    """

    def generate_random_sliding_tile(n):
        """Generates a random sliding tile puzzle given the size of the puzzle
        n: the number of rows and columns in the puzzle
        """
        # Create a list of all the possible numbers
        numbers = list(range(0, n * n))

        # Shuffle the list of numbers
        random.shuffle(numbers)

        # Shape the random array into a possible puzzle configuration
        tile_array = np.array(numbers).reshape(n, n).tolist()
        return tile_array

    def check_valid_sliding_tile(puzzle):
        """Checks to see if a sliding tile puzzle is valid (not all are)
        Uses some fancy math to see if they are possible
        """

        def count_inversions(array):
            count = 0
            for i in range(len(array)):
                j = i + 1
                while j < len(array):
                    if array[i] > array[j]:
                        count += 1
                    j += 1
            return count

        def blank_square_row(puzzle):
            for i in range(len(puzzle)):
                if 0 in puzzle[i]:
                    return i

        puzzle = np.array(puzzle)

        x_dim, y_dim = puzzle.shape

        # We are only considering square puzzles
        assert x_dim == y_dim

        # Flatten the matrix to just an array
        flattened_puzzle = puzzle.flatten()

        # Remove the Empty tile from the array
        flattened_puzzle = flattened_puzzle[flattened_puzzle != 0]

        # Get the number of inversions in the array
        inversions = count_inversions(flattened_puzzle)

        # Fancy math to see if the puzzle is solvable
        if x_dim % 2 == 0:
            return (blank_square_row(puzzle) + inversions) % 2 == 1
        else:
            return inversions % 2 == 0

    if n <= 1:
        raise ValueError("n must be greater than 1")

    # Generate a random puzzle
    puzzle = generate_random_sliding_tile(n)
    while not check_valid_sliding_tile(puzzle):
        puzzle = generate_random_sliding_tile(n)

    return SlidingTile(n, puzzle)
