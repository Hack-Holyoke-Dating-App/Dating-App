from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "there's nothing here."

@app.route("/hello")
def hello_word():
    return "Hello, word"

@app.route("/user/<rina>")
def show_user_profile(rina):
    print("Hi there")
    return 'User %s' % rina
