import numpy as np


class Sudoku:
    def __init__(
        self, arr: np.array = np.zeros((9, 9)), possibilities: np.array = None
    ):
        """Create a new Sudoku instance, by providing a 9 by 9 array that holds
        the starting position. Empty fields should be set to 0.

        :param arr: Input sudoku, 9×9 array-like object.
        :param possibilities: Mainly used to clone a sudoku directly.
        """

        self.possibilities = (
            np.array(
                [
                    [np.full(fill_value=True, shape=9) for _ in range(9)]
                    for __ in range(9)
                ]
            )
            if possibilities is None
            else possibilities
        )

        for i in range(9):
            for j in range(9):
                if arr[i, j] > 0:
                    self.setval(j, i, arr[i, j])

    def setval(self, x: int, y: int, num: int):
        """Set a value at (x, y)."""
        # remove option from all bounded numbers
        self.possibilities[y, :, num - 1] = 0
        self.possibilities[:, x, num - 1] = 0
        self.possibilities[
            y - y % 3 : y - y % 3 + 3, x - x % 3 : x - x % 3 + 3, num - 1
        ] = 0

        # set value itself
        self.possibilities[y, x] = np.array(
            [True if i == num - 1 else False for i in range(9)]
        )

    def update(self):
        """Update internal possibility array, following the sudoku rules."""
        while True:
            precount = np.sum(self.possibility_count())
            for y, x in np.argwhere(self.possibility_count() == 1):
                if self.is_valid():
                    self.setval(x, y, self.get_possibilities(x, y)[0])
                else:
                    return None

            if precount == np.sum(self.possibility_count()):
                break

    def __str__(self) -> str:
        """Nicely print the current state of the sudoku."""
        out = ""
        for row in self.possibilities:
            for col in row:
                if col.sum() == 1:
                    out += f"{np.arange(1, 10)[col][0]} "
                else:
                    out += "  "
            out += "\n"
        return out

    def possibility_count(self) -> int:
        """Returns number of options at each field."""
        return self.possibilities.sum(axis=2)

    def count_filled(self) -> int:
        """Total number of filled in fields."""
        return np.sum(self.possibility_count() == 1)

    def is_finished(self) -> bool:
        """Returns wheter the sudoku is solved yet."""
        return np.all(self.possibility_count() == 1)

    def is_valid(self) -> bool:
        """Checks if sudoku is still following the rules (and thus solveable)."""
        return 0 not in self.possibility_count()

    def get_possibilities(self, x, y) -> np.ndarray:
        """Returns the possible numbers at (x,y) in the sudoku."""
        return np.arange(1, 10)[self.possibilities[y, x]]

    def copy(self):
        return Sudoku(possibilities=self.possibilities.copy())

    def as_list(self) -> list:
        """Returns the sudoku as a list of rows."""
        return [
            [
                int(self.get_possibilities(x, y)[0])
                if len(self.get_possibilities(x, y)) == 1
                else 0
                for x in range(9)
            ]
            for y in range(9)
        ]

    def get_filled_positions(self) -> np.ndarray:
        """Get positions that are already filled."""
        return np.where(self.possibility_count() == 1)


def solve(sudoku: Sudoku, maxdepth: int = None, depth: int = 0) -> Sudoku:
    """Recursively solve a given sudoku until it is solved.

    :param sudoku: The unsolve Sudoku
    :param maxdepth: If set, the recursive solving will not go deeper than this
    :param depth: Recursive depth, mainly for debugging puposes.
    :return: The solved sudoku
    """

    # escape if solved
    if sudoku.is_finished():
        return sudoku

    # stop if maxdepth is reached
    if maxdepth is not None:
        if depth > maxdepth:
            return None

    if sudoku.is_valid():
        # loop through unsolved fields least choices first
        for y, x in np.argwhere(
            sudoku.possibility_count() == np.unique(sudoku.possibility_count())[1]
        ):
            for choice in sudoku.get_possibilities(x, y):
                # clone current state, to preserve if fails
                new_sudoku = sudoku.copy()
                new_sudoku.setval(x, y, choice)
                new_sudoku.update()

                # recursive solve
                solution = solve(new_sudoku, maxdepth=maxdepth, depth=depth + 1)
                if solution:
                    return solution


## GENERATE SUDOKUS
def generate(n: int = 10, maxdepth: int = 15) -> Sudoku:
    """Generates a solvable, non-filled sudoku with n prefilled fields.

    The algorithms is rather naive, and a single solution is not garanteed.

    :param n: number of prefilled-fields, defaults to 10
    :param maxdepth: how deep the solving of the generated sudoku should be tried, defaults to 15
    :return: Solveable sudoku
    """
    new_sudoku = generate_filled()

    while True:
        # pick n random positions
        random_positions = np.array([(x, y) for x in range(9) for y in range(9)])[
            np.random.choice(np.arange(81), n, replace=False)
        ]
        # create new test sudoku, with the numbers of new_sudoku at these positions
        test_sudoku = Sudoku()
        for (x, y) in random_positions:
            test_sudoku.possibilities[x, y] = new_sudoku.possibilities[x, y]
        # if the resulting sudoku is solvable, return it
        if solve(test_sudoku, maxdepth=maxdepth) is not None:
            return test_sudoku


def generate_filled() -> Sudoku:
    """Generates a randomly filled sudoku.

    It works by randomly setting the blocks on the first diagonal, and then it
    returns the first solution.

    :return: The filled sudoku.
    :rtpye: Sudoku
    """
    # create empty sudoku
    s = np.zeros((9, 9), dtype=np.uint8)
    # randomly fill blocks on diagonal, as they are independant, no danger for invalid sudokus
    rand_block = np.arange(1, 10).reshape((3, 3))
    np.random.shuffle(rand_block)
    s[:3, :3] = rand_block
    np.random.shuffle(rand_block)
    s[6:, 6:] = rand_block
    np.random.shuffle(rand_block)
    s[3:6, 3:6] = rand_block

    # Put in new Sudoku instance, and return first solution
    new_sudoku = Sudoku(s)
    return solve(new_sudoku)


if __name__ == "__main__":
    print(generate(15))
    test_sudoku = Sudoku(
        np.array(
            [
                [1, 0, 0, 0, 0, 0, 0, 0, 6],
                [0, 0, 6, 0, 2, 0, 7, 0, 0],
                [7, 8, 9, 4, 5, 0, 1, 0, 3],
                [0, 0, 0, 8, 0, 7, 0, 0, 4],
                [0, 0, 0, 0, 3, 0, 0, 0, 0],
                [0, 9, 0, 0, 0, 4, 2, 0, 1],
                [3, 1, 2, 9, 7, 0, 0, 4, 0],
                [0, 4, 0, 0, 1, 2, 0, 7, 8],
                [9, 0, 8, 0, 0, 0, 0, 0, 0],
            ]
        )
    )
    test_sudoku.update()
    print(test_sudoku)

    diff_sudoku = Sudoku(
        np.array(
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [2, 0, 0, 0, 0, 0, 0, 0, 0],
                [9, 6, 0, 0, 5, 8, 0, 0, 0],
                [0, 0, 3, 4, 0, 0, 0, 7, 0],
                [0, 0, 8, 0, 0, 0, 0, 0, 2],
                [0, 2, 0, 0, 6, 7, 5, 0, 0],
                [4, 0, 0, 9, 1, 0, 7, 5, 0],
                [0, 0, 0, 0, 0, 6, 0, 8, 0],
                [0, 0, 0, 0, 0, 5, 4, 0, 3],
            ]
        )
    )
    print(solve(diff_sudoku))
