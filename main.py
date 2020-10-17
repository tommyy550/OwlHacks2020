from flask import Flask, render_template, flash
import pyodbc
app = Flask(__name__)


conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-9MR2TVQ;'
                      'Database=GAINS;'
                      'Trusted_Connection=yes;')

@app.route("/")
def login():
    cursor = conn.cursor()
    # cursor.execute('''INSERT INTO GAINS.dbo.student(name) values('kellyfeng')''')
    # conn.commit()
    # cursor.execute('''UPDATE GAINS.dbo.student SET name='testupdate' WHERE id=31;''')
    # conn.commit()

    cursor.execute('SELECT * FROM GAINS.dbo.student')
    
    # retval="data:"
    # for row in cursor:
    #     for f in row:
        
    #         retval=retval+str(f)
    # return retval
    return render_template("login.html",cursor=cursor)

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
