from flask import Flask, render_template, session, request, flash, redirect

#import the connector function
from mysqlconnection import MySQLConnector

#import the regex module & set the email regex
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


app = Flask(__name__)
mysql = MySQLConnector(app, 'email_valid')
app.secret_key = 'FFFlask2020'

#sample query to test the db connection
# print mysql.query_db("SELECT * FROM emails")

@app.route('/', methods=["POST"])
def index():
    return render_template('index.html')

@app.route('/check', methods=["POST"])
def check():
    cEmail = request.form['email']
    session['email'] = cEmail
    if not EMAIL_REGEX.match(cEmail) or len(cEmail) < 2:
        flash ('Email is not valid')
        # for key in session.keys():
        #     session.pop(key)
        return redirect('/')
    else:
        data = {'email' : cEmail}
        query = "SELECT email FROM emails WHERE email = :email"
        compare = mysql.query_db(query,data)
        if not compare:
            query2 = "INSERT INTO emails (email, created_at, updated_at) VALUES (:email, NOW(), NOW() )"#add to db
            data = {'email' : cEmail}
            insert = mysql.query_db(query2,data)
            return redirect('/success')
        else:    
            return redirect('/success')
    

@app.route('/success')
def success():
    query3 = "SELECT email, DATE_FORMAT(created_at, '%m/%e/%y ' ' %h:%i%p' ) AS 'when' FROM emails"
    contains = mysql.query_db(query3)
    return render_template('success.html', contains = contains, email = session['email'] )

app.run(debug=True)