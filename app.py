import numpy as np
from flask import Flask, jsonify, redirect, render_template, request, url_for

from sudoku import Sudoku
from sudoku import solve as sudoku_solve

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/solve", methods=["POST", "GET"])
def solve():
    if request.method == "POST":
        raw_in = request.form.get("sudoku")
        rformat = request.form.get("return_format")
    elif request.args.get("s") is not None:
        raw_in = request.args.get("s")
        rformat = None
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

    # select return format
    rformat = rformat or request.args.get("format", "text")
    if rformat == "text":
        return f"{solved_sudoku}"
    elif rformat == "html":
        return render_template("sudoku_render.html", sudoku=solved_sudoku.as_list())
    elif rformat == "json":
        return jsonify(
            {
                "original_sudoku": new_sudoku.as_list(),
                "solved_sudoku": solved_sudoku.as_list(),
            }
        )
    else:
        return f"Not valid format: {rformat}. Use 'text' 'html' or 'json'."


# to run as dev server
if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True)