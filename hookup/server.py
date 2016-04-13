import hashlib
import psycopg2
import psycopg2.extras
import os
import sys 
from flask import Flask, session, redirect, url_for, request, render_template,escape
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.secret_key= os.urandom(24).encode('hex')



def connectToDB():
    connectionString='dbname=hookup user=postgres password=maher123 host=localhost'
    print connectionString
    try:
        return psycopg2.connect(connectionString)
    except:
        print ("Can't connect to database")

@app.route('/', methods=['GET', 'POST'])
def mainIndex():
    conn=connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    print "we here"
    if 'username' in session:
        print "we here 3"
        #session.pop('username', None)
        #username_session = escape(session['username']).capitalize()
        return redirect(url_for('homePage',session_user_name=session['username']))
    if request.method == 'POST':
        print "we here test",request.form['username'],request.form['password']
        if 'submit' in request.form:
            print "we here 2"
            username = request.form['username']
            currentUser = username
            pw = request.form['password']
            print pw
            query = "select * from users WHERE username = '%s' AND password = '%s'" % (username, pw)
            print query
            cur.execute(query)
            r=cur.fetchall()
            if not r:
                return render_template('index.html')
                
            if r:
                session['username'] = request.form['username']
                for n in r:
                    zipmain= n['zipcode']
                session['zipm']=zipmain
            return redirect(url_for('homePage',session_user_name=session['username']))
           
         #return redirect(url_for('mainIndex',user=currentUser,c=ch))
        if 'register' in request.form:
            print "register"
    
    return render_template('index.html')



@app.route('/profile', methods=['GET', 'POST'])
def profile():
    conn=connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if 'username' in session:
        query = "select * from users WHERE username = '%s'" % (session['username'])
        cur.execute(query)
        res=cur.fetchall()
        return render_template('profile.html',res=res)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('mainIndex'))

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route('/HomePage')
def homePage():
    if "username" in session:
        return render_template('home.html')
    return render_template('index.html')
        

if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=8080)