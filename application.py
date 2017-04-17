from flask import make_response
from flask import render_template, request, session
from src.common.database import Database
from src.models.blog import Blog
from src.models.user import User

__author__ = 'jmgamao'
from flask import Flask


app = Flask(__name__) #__main__
app.secret_key = 'abz'

@app.before_first_request # run method before the 1st request
def initialize_database():
    Database.initialize()

@app.route('/') # www.mysite.com/api/
def home():
    return render_template('base.html')

@app.route('/login') # Login
def login():
    return render_template('login.html')

@app.route('/register') # Register
def register():
    return render_template('register.html')


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


@app.route('/blogs/<string:user_id>')
@app.route('/blogs')
def user_blogs(user_id=None):
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session.get('email'))
    blogsx = user.get_blogs()

    return render_template("user_blogs.html", blogs=blogsx, email = user.email)

@app.route('/posts/<string:blog_id>')
def blog_posts(blog_id):
    blog = Blog.from_mongo(blog_id)
    posts = blog.get_posts()

    return render_template('posts.html', posts=posts, blog_title=blog.title)


@app.route('/blogs/new', methods=['POST', 'GET'])
def create_new_blog():
    if request.method == 'GET':
        return  render_template('new_blog.html')
    else:
        title = request.form['title']
        description = request.form['description']
        user = User.get_by_email(session.get('email'))
        user.new_blog(title, description)

        return make_response(user_blogs(user._id))




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