from flask import render_template, request, session

from src.common.database import Database
from src.models.user import User

__author__ = 'jmgamao'
from flask import Flask


app = Flask(__name__) #__main__
app.secret_key = 'abz'

@app.route('/') # www.mysite.com/api/
def home():
    return render_template('base.html')

@app.route('/login') # Login
def login():
    return render_template('login.html')

@app.route('/register') # Register
def register():
    return render_template('register.html')

@app.before_first_request # run method before the 1st request
def initialize_database():
    Database.initialize()


@app.route('/auth/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email, password):
        User.login(email)
    else:
        session['email'] = None

    return render_template("profile.html", email = session.get('email'))



@app.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']
    User.register(email,password)

    return render_template('profile.html', email = session.get('email'))

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

if __name__ == '__main__':
   ## app.run(debug=True)
    app.run(port=4990, debug=True)