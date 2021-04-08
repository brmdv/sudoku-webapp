from flask import Flask, render_template, request

app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/solve", methods=["POST"])
def solve():
    raw_in=request.form.get("sudoku")
    return f"Solving not implemented yet. Here is your sudoku back:\n\n{raw_in}"