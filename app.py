from flask import Flask, render_template, request, redirect, url_for
from sudoku import Sudoku, solve
import numpy as np

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/solve", methods=["POST"])
def solve():
    # clean input sudoku, only leave mubers
    try:
        sudoku_text = np.array(
            [int(c) for c in request.form.get("sudoku") if c in "0123456789"]
        ).reshape(9, 9)
    except ValueError as exception:
        return f"Not a valid sudoku, try again."

    new_sudoku = Sudoku(sudoku_text)

    return f"{new_sudoku}"