from flask import Flask, render_template, jsonify
from flaskext.mysql import MySQL  # import mysql
import json

app = Flask(__name__)

# mysql config
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'user'
app.config['MYSQL_DATABASE_HOST'] = 'localhost:3306'
mysql.init_app(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/getUser')
def getUser():
    # mysql connection
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * from user")
    data = cursor.fetchone()
    return data


@app.route('/status')
def getStatus():
    #response.headers['Content-Type'] = 'application/json'
    return jsonify({'tasks': 'hello'})


if __name__ == '__main__':
    app.run(debug=True)
