from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from datetime import date
import random
import MySQLdb.cursors
import re

app = Flask(__name__)


app.secret_key = 'roger that'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'hotel'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/booking', methods =['GET', 'POST'])
def booking():
    msg=''
    if request.method == 'POST' and 'name' in request.form and 'mobile' in request.form and 'address' in request.form and 'checkin' in request.form and 'checkout' in request.form and 'number_of_rooms' in request.form and 'room_type' in request.form and 'price' in request.form and 'mode' in request.form:
        name = request.form['name']
        mobile = request.form['mobile']
        address = request.form['address']
        checkin = request.form['checkin']
        checkout = request.form['checkout']
        number_of_rooms = request.form['number_of_rooms']
        room_type = request.form['room_type']
        price = request.form['price']
        mode = request.form['mode']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO book VALUES (NULL,%s, %s, %s, %s, %s, %s, %s, %s, %s)', (name, mobile, address, checkin, checkout, number_of_rooms, room_type, price, mode))
        mysql.connection.commit()
        msg = 'Booking Successful'
        return render_template('index.html', msg=msg)
    return render_template('booking.html')

@app.route('/guestlist')
def guestlist():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM book')
    guestdata = cursor.fetchall()
    return render_template('guestlist.html', guestdata=guestdata)

@app.route('/roomsinfo')
def roomsinfo():
    return render_template('roomsinfo.html')

@app.route('/roomservice')
def roomservice():
    return render_template('roomservice.html')

@app.route('/verifyguestid', methods =['GET', 'POST'])
def verifyguestid():
    if request.method == 'POST' and 'guestid' in request.form:
        guestid = request.form['guestid']   
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM book WHERE id = %s', (guestid,))
        guestdata = cursor.fetchone()
        if guestdata is None:
            return 1
        else:
            return guestdata                                                           

def getroomtype(roomtype):
    if roomtype == '1':
        return 'Single Room Non Ac'
    elif roomtype == '2':
        return 'Double Room Non Ac'
    elif roomtype == '3':
        return 'Single Room Ac'
    elif roomtype == '4':
        return 'Double Room Ac'
app.jinja_env.globals.update(getroomtype=getroomtype) 
