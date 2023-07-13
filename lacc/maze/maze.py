import copy
import enum

from lacc.module3.board import Board


class Maze(enum.Enum):
    WALL = "#"
    START = "S"
    GOAL = "G"
    FLOOR = " "
    EXPLORED = "E"


class Direction(enum.Enum):
    UP = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()


UP = Direction.UP
DOWN = Direction.DOWN
LEFT = Direction.LEFT
RIGHT = Direction.RIGHT


class MazeBoard(Board):
    def __init__(self, raw_board):
        board = [[Maze(e) for e in row] for row in raw_board]
        super().__init__(board)

        self.me = self.start
        self._explored = set()
        self._breadcrumbs = list()

        self._highlights = set()

    def __deepcopy__(self, memo):
        cpy = MazeBoard(copy.deepcopy(self.data, memo))
        cpy.me = copy.deepcopy(self.me, memo)
        cpy._explored = copy.deepcopy(self._explored, memo)
        cpy._breadcrumbs = copy.deepcopy(self._breadcrumbs, memo)
        cpy._highlights = copy.deepcopy(self._highlights, memo)
        cpy._snapshots = self._snapshots
        return cpy

    @property
    def start(self):
        for r, row in enumerate(self._board):
            for c, cell in enumerate(row):
                if cell == Maze.START:
                    return r, c
        raise RuntimeError("Cannot find maze start.")

    @property
    def goal(self):
        for r, row in enumerate(self._board):
            for c, cell in enumerate(row):
                if cell == Maze.GOAL:
                    return r, c
        raise RuntimeError("Cannot find maze goal.")

    @property
    def highlights(self):
        return self._highlights

    @property
    def breadcrumbs(self):
        return self._breadcrumbs

    @property
    def explored(self):
        return self._explored

    def reset(self):
        super().reset()
        self.me = self.start
        self._breadcrumbs.clear()
        self._explored.clear()
        self._highlights.clear()

    def explore(self, pos):
        self._explored.add(pos)

    def move(self, direction):
        self.me = self.to_my(direction)

    def have_we_explored(self, pos):
        return pos in self._explored

    def drop_breadcrumb(self):
        self._breadcrumbs.append(self.me)

    def pick_up_breadcrumb(self):
        self._breadcrumbs.pop()

    def to_my(self, direction):
        x, y = self.me
        if direction == Direction.UP:
            return (x - 1, y)
        elif direction == Direction.DOWN:
            return (x + 1, y)
        elif direction == Direction.LEFT:
            return (x, y - 1)
        elif direction == Direction.RIGHT:
            return (x, y + 1)
        raise RuntimeError()

    def highlight(self, coord):
        self._highlights.add(coord)

    def clear_highlights(self):
        self._highlights.clear()
