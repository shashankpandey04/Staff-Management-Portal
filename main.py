#Staff Management Portal
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector as msc

mycon=msc.connect(host='localhost',user='root',passwd='root',database='aws')
mycur=mycon.cursor()
app = Flask(__name__)

app.secret_key = 'any random string'
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['uname']
        passwd = request.form['passwd']
        try:
            mycur.execute(f"SELECT * FROM login WHERE uname='{uname}' AND passwd='{passwd}' AND admin='1'")
            admin_res = mycur.fetchone()
            if admin_res:
                session['uname'] = uname
                session['admin'] = True
                return redirect(url_for('dashboard'))
        except:
            pass 
        try:
            mycur.execute(f"SELECT * FROM login WHERE uname='{uname}' AND passwd='{passwd}'")
            user_res = mycur.fetchone()
            if user_res:
                session['uname'] = uname
                return redirect(url_for('dashboard'))
        except:
            pass 
        return render_template('index.html', msg='Invalid Username or Password')
    else:
        return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'admin' in session:
        return render_template('dashboard.html', session=session)
    if 'uname' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html', session=session)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

app.run(debug=True)