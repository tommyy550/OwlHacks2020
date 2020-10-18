from flask import Flask, render_template,request, redirect, session, url_for, flash, abort
import pyodbc
from datetime import date
app = Flask(__name__)


conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-9MR2TVQ;'
                      'Database=GAINS;'
                      'Trusted_Connection=yes;')

@app.route("/",methods = ['POST', 'GET'])
def login():
    if request.method=='POST':

        cursor = conn.cursor()
    # cursor.execute('''INSERT INTO GAINS.dbo.student(name) values('kellyfeng')''')
    # conn.commit()
    # cursor.execute('''UPDATE GAINS.dbo.student SET name='testupdate' WHERE id=31;''')
    # conn.commit()
        username = request.form['loginUser']
        cursor.execute("SELECT * FROM GAINS.dbo.donors WHERE username='"+username+"'")
        user_id=""
        totalPoints=0
        for row in cursor:
            user_id=row[0]
            totalPoints=row[3]

        session['user_id'] =user_id
        session['totalPoints']=totalPoints
        return render_template("about.html")
    
    return render_template("login.html")

@app.route("/create",methods = ['POST', 'GET'])
def create():
    if request.method=='POST':
        username = request.form['username']
        password= request.form['password']
        cursor = conn.cursor()
        cursor.execute("INSERT INTO GAINS.dbo.donors(username,password,totalPoints) values('"+username+"','"+password+"',0)")
        conn.commit()
        
        return render_template("login.html")
    
    return render_template("create.html")

@app.route("/leaderboard")
def leaderboard():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT username, SUM(Amount) AS Total_Donations
        FROM donors
        JOIN Donations
        ON donors.UserId = Donations.UserId
        GROUP BY username
        ORDER BY Total_Donations DESC
        """)

    return render_template("leaderboard.html",leaderboardDetails=cursor)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/donate",methods = ['POST', 'GET'])
def donate():
    id=session["user_id"]
    if request.method=='POST':
        today_date=date.today()
        amount=request.form['amount']
        cursor = conn.cursor()
        cursor.execute("INSERT INTO GAINS.dbo.Donations(UserId,Amount,date) values('"+str(id)+"','"+str(amount)+"','"+str(today_date)+"')")
        conn.commit()

    
    cursor = conn.cursor()
    # userDetails=cursor.execute("SELECT * FROM GAINS.dbo.donors WHERE UserId='"+str(id)+"'")
    
    cursor.execute("SELECT * FROM GAINS.dbo.Donations WHERE UserId='"+str(id)+"' ORDER BY date DESC")

    return render_template("donate.html",donationDetails=cursor)
    
if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(debug=True)
