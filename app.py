import os

from flask import Flask

app = Flask(__name__)

# Load configuration
app.config['MONGO_URI'] = os.environ['MONGO_URI']

@app.route("/")
def hello():
    return "hello world"
