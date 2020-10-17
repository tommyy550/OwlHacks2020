from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def login():
    return render_template("login.html")

@app.route("/create")
def create():
    return render_template("create.html")

@app.route("/leaderboard")
def leaderboard():
    return render_template("leaderboard.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/donate")
def donate():
    return render_template("donate.html")
    
if __name__ == "__main__":
    app.run(debug=True)
