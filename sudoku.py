import numpy as np


class Sudoku:
    def __init__(self, arr: np.array = np.zeros((9, 9)), possibilities=None):
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

    def setval(self, x, y, num):

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

    def update(self, depth=0):
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
        out = ""
        for row in self.possibilities:
            for col in row:
                if col.sum() == 1:
                    out += f"{np.arange(1, 10)[col][0]} "
                else:
                    out += "  "
            out += "\n"
        return out

    def possibility_count(self):
        return self.possibilities.sum(axis=2)

    def count_filled(self):
        return np.sum(self.possibility_count() == 1)

    def is_finished(self):
        return np.all(self.possibility_count() == 1)

    def is_valid(self):
        return 0 not in self.possibility_count()

    def get_possibilities(self, x, y):
        return np.arange(1, 10)[self.possibilities[y, x]]

    def copy(self):
        return Sudoku(possibilities=self.possibilities.copy())

    def as_list(self):
        return [
            [
                int(self.get_possibilities(x, y)[0])
                if len(self.get_possibilities(x, y)) == 1
                else 0
                for x in range(9)
            ]
            for y in range(9)
        ]


def solve(sudoku, depth=0, max_depth=None):

    # escape if solved
    if max_depth is not None:
        if depth >= max_depth:
            return None
    if sudoku.is_finished():
        return sudoku

    if sudoku.is_valid():
        # loop through unsolved fields least choices first

        for y, x in np.argwhere(
            sudoku.possibility_count() == np.unique(sudoku.possibility_count())[1]
        ):
            for choice in sudoku.get_possibilities(x, y):
                new_sudoku = sudoku.copy()
                new_sudoku.setval(x, y, choice)
                new_sudoku.update()

                solution = solve(new_sudoku, depth=depth + 1, max_depth=max_depth)
                if solution:
                    return solution
            return None


if __name__ == "__main__":
    very_diff_sudoku = Sudoku(
        np.array(
            [
                [0, 0, 0, 0, 0, 3, 0, 1, 7],
                [0, 1, 5, 0, 0, 9, 0, 0, 8],
                [0, 6, 0, 0, 0, 0, 0, 2, 0],
                [1, 0, 0, 0, 0, 7, 0, 0, 0],
                [0, 0, 9, 0, 0, 0, 2, 0, 0],
                [0, 0, 0, 5, 0, 0, 0, 0, 4],
                [0, 0, 0, 0, 0, 0, 0, 2, 0],
                [5, 0, 0, 6, 0, 0, 3, 4, 0],
                [3, 4, 0, 2, 0, 0, 0, 0, 0],
            ]
        )
    )
    solved_vds = solve(very_diff_sudoku)

    print(str(very_diff_sudoku))
    print(str(solved_vds))