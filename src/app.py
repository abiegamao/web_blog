__author__ = 'jmgamao'
from flask import Flask


app = Flask(__name__) #__main__

@app.route('/') # www.mysite.com/api/
def hello_method():
    return 'hello world!'

@app.route('/users') # www.mysite.com/api/
def hello():
    return 'hello users!'

if __name__ == '__main__':
    app.run(port=4995)