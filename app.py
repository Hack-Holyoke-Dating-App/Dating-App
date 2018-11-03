import os

from flask import Flask

app = Flask(__name__)

# Load configuration
app.config['MONGO_URI'] = os.environ['MONGO_URI']

# Setup MongoDB
mongo = PyMongo(app)

@app.route("/")
def hello():
    return "there's nothing here."

@app.route("/hello")
def hello_word():
    return "Hello, word"

@app.route("/user/<rina>")
def show_user_profile(rina):
    return 'User %s' % rina
