import collections
import copy


def is_iter(i, ignore_string=True):
    if ignore_string and isinstance(i, str):
        return False
    try:
        iter(i)
    except TypeError:
        return False
    else:
        return True


class Board(collections.UserList):
    """A 2D grid."""

    def __init__(self, board_state=None, rows=None, cols=None, default=None):
        has_init_state = board_state is not None
        has_empty_state = rows is not None and cols is not None
        if not has_init_state and not has_empty_state:
            raise ValueError(
                "A board must have it's initial state set or given the number of rows and columns."
            )

        if has_init_state:
            self._check_is_valid_board(board_state)
            self._board = board_state
            self._num_rows = len(board_state)
            self._num_cols = len(board_state[0])
        else:
            if is_iter(default):
                raise ValueError("Default value cannot be an iterable.")
            self._board = [[default for _ in range(cols)] for _ in range(rows)]
            self._num_rows = rows
            self._num_cols = cols

        super().__init__(copy.deepcopy(self._board))

        self._snapshots = list()

    def __getitem__(self, loc):
        if isinstance(loc, tuple):
            r, c = loc
            return self[r][c]
        return super().__getitem__(loc)

    @property
    def rows(self):
        return self

    @property
    def cols(self):
        return [
            [self[r][c] for r in range(self.num_rows)] for c in range(self.num_cols)
        ]

    @property
    def num_rows(self):
        return self._num_rows

    @property
    def num_cols(self):
        return self._num_cols

    @property
    def snapshots(self):
        return self._snapshots

    def snapshot(self):
        self._snapshots.append(copy.deepcopy(self))

    def reset(self):
        self.data = copy.deepcopy(self._board)
        self._snapshots.clear()

    def _check_is_valid_board(self, board_state):
        # Check entire 2D array.
        if not isinstance(board_state, list):
            raise ValueError("A board must be a 2D list.")

        # Check each row.
        for ir, r in enumerate(board_state):
            if not isinstance(r, list):
                raise ValueError(f"Row {ir} of a board must be a 1D list.")

            # Check each element.
            for ic, c in enumerate(r):
                if is_iter(c):
                    raise ValueError(
                        f"Element {c} at [{ir}, {ic}] of type {type(c)} cannot be iterable."
                    )

        # Verify board dimensions are the same for each row.
        row_lens = [len(r) for r in board_state]
        uniq_row_lens = set(row_lens)
        if len(row_lens) == 0:
            raise ValueError("A board must have at least one row.")
        elif len(uniq_row_lens) != 1:
            raise ValueError(
                "Each row in the board must have the same number of columns."
            )
        elif list(uniq_row_lens)[0] == 0:
            raise ValueError("A board must have at least one column.")
