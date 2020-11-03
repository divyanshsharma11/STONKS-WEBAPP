from flask import Flask, render_template, request, session, redirect, url_for, send_file
import app.Auth as Auth
import app.excel_generator as CSV
import app.grap_generator as gg


app = Flask(__name__)
app.secret_key = 'afhebcjkhvieuuweh74g273t23ug'


@app.route("/")
def index():
    return render_template('login.html')


@app.route("/login")
def loginpage():
    return render_template('login.html')


@app.route("/signup")
def signuppage():
    return render_template('signup.html')


@app.route("/AuthLogin", methods=['POST'])
def login():
    username = request.form['user_name']
    userpin = request.form['user_pin']

    chechAuth = Auth.authLogin(username, userpin)

    print(chechAuth)

    if chechAuth is True:
        session['username'] = username
        return redirect(url_for('profile'))

    else:
        return render_template('login.html', error=True)


@app.route("/AuthSign", methods=['POST'])
def sign():
    username = request.form['user_name']
    userpin = request.form['user_pin']

    userExists = Auth.checkUserExists(username)

    if userExists is True:
        return render_template('signup.html', error=True, error_text="username already exists")

    elif(userpin == ''):
        return render_template('signup.html', error=True, error_text="userpin is required")

    else:
        session['username'] = username
        Auth.authSign(username, userpin)
        Auth.createuserbase(username)
        stock_array = []
        return redirect(url_for('profile'))


@app.route("/addstock", methods=['POST'])
def addstock():
    stock = request.form['new_stock']
    print(stock)
    Auth.addstock(stock, session.get('username'))

    return redirect(url_for('profile'))


@app.route("/deletestock", methods=['POST'])
def deletestock():
    stock = request.form['delete_stock']
    print(stock)
    Auth.deletestock(stock, session.get('username'))

    return redirect(url_for('profile'))


@app.route("/profile")
def profile():

    if(session.get('username') != None):
        stock_array = Auth.getstocks(session.get('username'))
        return render_template('profile.html', user_name=session.get('username'), stock=stock_array)

    else:
        return redirect(url_for('loginpage'))


@app.route("/stock/<stock_name>")
def stock(stock_name):

    if(session.get('username') != None):
        print(stock_name)
        CSV.generateCsv(session.get('username'), stock_name)
        gg.graphPlot(session.get('username'), stock_name)
        data = Auth.getStockData(stock_name)
        return render_template('stock_page.html', stock_name=stock_name, stock=stock_name, data=data, user_name=session.get('username'))

    else:
        return redirect(url_for('loginpage'))


@app.route("/signout")
def signout():
    print("signout init..")
    CSV.deleteFolder(session.get('username'))
    session.pop('username')

    return render_template('login.html')


@app.route("/plot")
def plot():

    gg.graphPlot()
    return("working")
