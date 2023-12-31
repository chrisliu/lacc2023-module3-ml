import copy
import enum

from lacc.board import Board


class Maze(enum.Enum):
    WALL = "#"
    START = "S"
    GOAL = "G"
    FLOOR = " "
    EXPLORED = "E"

    def __eq__(self, other):
        if isinstance(other, Maze):
            return super().__eq__(other)
        else:
            return self.value == other

    def __hash__(self):
        return super().__hash__()


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
        self.explored = set()
        self._breadcrumbs = list()

        self._highlights = set()

    def __deepcopy__(self, memo):
        cpy = MazeBoard(copy.deepcopy(self.data, memo))
        cpy.me = copy.deepcopy(self.me, memo)
        cpy.explored = copy.deepcopy(self.explored, memo)
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

    def reset(self):
        super().reset()
        self.me = self.start
        self._breadcrumbs.clear()
        self.explored.clear()
        self._highlights.clear()
        self._snapshots.clear()

    def explore(self, pos):
        self.explored.add(pos)

    def move(self, direction):
        self.me = self.to_my(direction)

    def have_we_explored(self, pos):
        return pos in self.explored

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

    def _repr_pretty_(self, p, cycle):
        p.pretty([[c.value for c in row] for row in self])
