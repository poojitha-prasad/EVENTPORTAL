from flask import Flask, render_template, request, redirect, url_for, session,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import json

from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import sys
import time


app = Flask(__name__)

app.config.from_pyfile('config.cfg')

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'meenu1234'
app.config['MYSQL_DB'] = 'buildfh'



mysql = MySQL(app)

mail = Mail(app)

s = URLSafeTimedSerializer('Thisisasecret!')

@app.route('/')


@app.route('/welcome')
def welcome():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(' SELECT eventtitle,eventdatetime FROM eventstable WHERE eventdatetime > NOW() ORDER BY eventdatetime')
    eventdetailsw=cursor.fetchall()
    return render_template('bfhwel1.html',eventdetailsw=eventdetailsw)

@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return redirect(url_for('loginhome',msg=msg))



        else:
            msg = 'Incorrect username / password !'
    return render_template('bfhlog1.html', msg = msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'semester' in request.form and 'branch' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        semester = request.form['semester']
        branch = request.form['branch']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email or not semester or not branch:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts (id,username,password,email,semester,branch) VALUES (NULL, % s, % s, % s, % s, % s)', (username, password, email,semester,branch, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('bfhreg.html', msg = msg)

@app.route('/loginhome')
def loginhome():
   if session['loggedin'] == True:
    username=session['username']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE username = %s',(username,))
    accountd=cursor.fetchall()
    cursor.execute('SELECT eventstable.eventtitle AS et,eventstable.eventdatetime AS ed, eventstable.eventlocation AS cee from eventstable INNER JOIN eventregister ON eventstable.eventtitle=eventregister.eventtitle WHERE eventregister.username=%s and eventstable.eventdatetime > NOW() GROUP BY eventregister.eventtitle ORDER BY eventstable.eventdatetime',(username,))
    eventdetailslh=cursor.fetchall()
    return render_template('bfhbase1.html',eventdetailslh=eventdetailslh,accountd=accountd)

@app.route('/attendance')
def attendance():
    if session['loggedin'] == True:
        username=session['username']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT confirm.eventtitle as eve FROM confirm INNER JOIN eventstable ON confirm.eventtitle=eventstable.eventtitle WHERE confirm.username=%s and confirm.confirm="yes" and eventstable.eventdatetime < NOW() ORDER BY eventstable.eventdatetime ',(username,))
        attended=cursor.fetchall()
        return render_template('bfhattendance.html',attended=attended)

@app.route('/addevent', methods =['GET', 'POST'])
def  addevent():
 if session['loggedin'] == True:
    msg = ''
    if request.method == 'POST'  and  "Event_Title" in request.form and "DateTime" in request.form  and "Location"  in request.form and "maxnum" in request.form and    "Event_desc" in request.form :

             Event_Title= request.form["Event_Title"]
             DateTime= request.form["DateTime"]
             Location=request.form["Location"]
             maxnum = request.form["maxnum"]

             Event_desc= request.form["Event_desc"]
             cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
             cursor.execute('SELECT * FROM eventstable WHERE eventtitle=%s and eventlocation=%s', (Event_Title,Location, ))
             eventstable= cursor.fetchone()

             if eventstable:
               msg = 'Event already exists !'
             elif not Event_Title or not DateTime or not Location or not maxnum or not Event_desc:
                 msg = 'Please fill out the form !'
             else:

                 Event_Title=request.form['Event_Title']
                 print(Event_Title)

                 cursor.execute('INSERT INTO eventstable VALUES (NULL, % s, % s, % s,%s,%s)', (Event_Title, DateTime,Location,maxnum, Event_desc, ))
                 mysql.connection.commit()
                 msg='Event Successfully Added!'

    return render_template('bfhaddevent.html', msg =msg)



@app.route('/regevent',methods =['GET', 'POST'])
def regevent():
  if session['loggedin'] == True:
      msga=''
      username=session['username']
      cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      cursor.execute('SELECT eventtitle FROM eventstable WHERE eventdatetime > NOW()')
      eventname=cursor.fetchall()


      if request.method == 'POST' and 'eventsnamea' in request.form:
          eventsnamea=request.form['eventsnamea']
          session['eventtitle']=eventsnamea
          cursor.execute('Select email from accounts where username=% s',(username,))
          em=cursor.fetchone()
          email=em.get("email")
          session['email']=email
          cursor.execute('SELECT maxpart FROM eventstable WHERE eventtitle= % s',(eventsnamea,))
          a=cursor.fetchone()
          aa=a.get("maxpart")
          an=float(aa)
          cursor.execute('SELECT count(*) FROM eventregister where eventtitle = % s',(eventsnamea,))
          b=cursor.fetchone()
          ba=b.get("count(*)")
          bn=float(ba)
          cursor.execute('SELECT * FROM eventregister WHERE username = % s and eventtitle = % s', (username,eventsnamea, ))
          accounta=cursor.fetchone()
          if accounta:
              msga='You have already registered for ths event'
          elif not eventsnamea:
              msga='Please select an event to register'
          elif an <= bn:
              msga='The Event reached maximum no:of participants'

          else:
             cursor.execute('INSERT INTO confirm (confirm,email,username,eventtitle) VALUES ("not confirmed",% s,% s,% s)', (email,username,eventsnamea, ))
             cursor.execute('INSERT INTO eventregister VALUES (%s ,%s) ',(username,eventsnamea,))
             mysql.connection.commit()
             msga = 'You have successfully registered !An email has been sent to your mail. Please confirm your attendance the day before the event.'

             token = s.dumps(email, salt='email-confirm')
             session['token']=token

             msg = Message('Confirm Email', sender='pdpprojectmail@gmail.com', recipients=[email])

             link = url_for('confirm_email', token=token, _external=True)

             msg.body = 'Link will be active for only one hour.Your link is {}'.format(link)

             mail.send(msg)

      elif request.method == 'POST':
          msga = 'Please fill out the form !'
      return render_template('bfhregevent1.html',eventname=eventname,msga=msga)

@app.route('/confirm_email',methods=['GET', 'POST'])
def confirm_email():
    msg=''
    token=session['token']
    email=session['email']
    username=session['username']
    eventtitle=session['eventtitle']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select date(eventdatetime) as eventdate from eventstable where eventtitle= % s', (eventtitle,))
    eventdate=cursor.fetchone()
    date=eventdate.get("date(eventdatetime)")
    try:
        email = s.loads(token, salt='email-confirm', max_age=date)
    except SignatureExpired:
        return render_template('bfhexpire.html')
    if request.method =='POST' and 'yn' in request.form:
        yn=request.form['yn']
        cursor.execute('SELECT * FROM confirm WHERE email = % s and eventtitle =% s and username= % s and confirm in ("yes","no")', (email,eventtitle,username, ))
        accounta=cursor.fetchone()
        if accounta:
            msg='You have already given the confirmation'
            return render_template('bfhcheckmsg2.html')
        elif not yn:
            msg='Please select an option'
        else:
            cursor.execute('UPDATE confirm SET confirm=% s WHERE email=% s and username = % s and eventtitle =% s ', (yn,email,username,eventtitle, ))

            mysql.connection.commit()
            return render_template('bfhcheckmsg.html')
    return render_template('bfhcheck.html',token=token,email=email,msg=msg,eventtitle=eventtitle)


@app.route('/events',methods =['GET', 'POST'])
def events():
  if session['loggedin'] == True:
      msg=''
      eventp=''
      cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      cursor.execute('SELECT * FROM eventstable WHERE eventdatetime > NOW() ORDER BY eventdatetime')
      eventdetails=cursor.fetchall()
      cursor.execute('SELECT eventtitle FROM eventstable WHERE eventdatetime > NOW()')
      eventname=cursor.fetchall()
      eventpp=''
      if request.method == 'POST' and 'eventp' in request.form:
       eventp=request.form['eventp']
       cursor.execute('SELECT username FROM eventregister WHERE eventtitle = % s',(eventp,))
       eventpp=cursor.fetchall()
       if not eventp:
           msg="Select an Event"
      return render_template('bfhevents.html',eventdetails=eventdetails,eventname=eventname,eventpp=eventpp,msg=msg,eventp=eventp)






if __name__ == "__main__":
    app.run(debug(True))
