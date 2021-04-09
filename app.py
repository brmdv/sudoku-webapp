from flask import Flask, render_template, request, redirect, url_for
from sudoku import Sudoku
from sudoku import solve as sudoku_solve
import numpy as np

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/solve", methods=["POST", "GET"])
def solve():
    if request.method == "POST":
        raw_in = request.form.get("sudoku")
    elif request.args.get("s") is not None:
        raw_in = request.args.get("s")
    else:
        return redirect(url_for("index"))

    # clean input sudoku, only leave mubers
    try:
        sudoku_text = np.array([int(c) for c in raw_in if c in "0123456789"]).reshape(
            9, 9
        )
    except ValueError as exception:
        return f"Not a valid sudoku, try again."

    new_sudoku = Sudoku(sudoku_text)
    solved_sudoku = sudoku_solve(new_sudoku)

    return f"{solved_sudoku}"