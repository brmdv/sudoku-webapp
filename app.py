import numpy as np
from flask import Flask, jsonify, redirect, render_template, request, url_for, Response

from sudoku import Sudoku, generate
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
    if not new_sudoku.is_valid():
        return f"Sudoku is not valid, try again."

    #  SOLVE
    solved_sudoku = sudoku_solve(new_sudoku, max_depth=100)
    if solved_sudoku is None:
        return f"Sudoku not solveable, check input."

    # select return format
    rformat = rformat or request.args.get("format", "text")
    if rformat == "text":
        return Response(str(solved_sudoku), mimetype="text/plain")
    elif rformat == "html":
        return render_template(
            "show_sudoku.j2", sudoku=solved_sudoku.as_list(), title="Solution"
        )
    elif rformat == "pure_html":
        return render_template("render_sudoku.html", solved_sudoku.as_list())

    elif rformat == "json":
        return jsonify(
            {
                "original_sudoku": new_sudoku.as_list(),
                "solved_sudoku": solved_sudoku.as_list(),
            }
        )
    else:
        return f"Not valid format: {rformat}. Use 'text' 'html' or 'json'."


@app.route("/generate")
def generate_sudoku():
    try:
        n = int(request.args.get("n", 15))
        assert n <= 81
        assert n >= 0
    except:
        return "Not valid n."
    sud = generate(n)

    # select return format
    rformat = request.args.get("format", "html")
    if rformat == "text":
        return Response(str(sud), mimetype="text/plain")

    elif rformat == "html":
        return render_template(
            "show_sudoku.j2", sudoku=sud.as_list(), title="New sudoku"
        )
    elif rformat == "json":
        return jsonify(
            {
                "new_sudoku": sud.as_list(),
                "solution": sudoku_solve(sud).as_list(),
            }
        )
    else:
        return f"Not valid format: {rformat}. Use 'text' 'html' or 'json'."
    return render_template


# to run as dev server
if __name__ == "__main__":
    import os

    # You want to put the value of the env variable PORT if it exist (some services only open specifiques ports)
    port = int(os.environ.get("PORT", 5000))
    # Threaded option to enable multiple instances for
    # multiple user access support
    # You will also define the host to "0.0.0.0" because localhost will only be reachable from inside de server.
    app.run(host="0.0.0.0", threaded=True, port=port)
