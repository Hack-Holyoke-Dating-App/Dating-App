import os

from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

import models

app = Flask(__name__)

# Load configuration
app.config['MONGO_URI'] = os.environ['MONGO_URI']

# Setup MongoDB
mongo = PyMongo(app)

@app.route("/api/users", methods=['POST'])
def create_user():
    req_user = request.json['user']

    user = models.User(id=None,
                       username=req_user['username]',
                       name=req_user['name'],
                       profile_picture_url=None,
                       age=req_user['age'],
                       location=req_user['location'])

    inserted_user = mongo.db.users.insert(user.to_dict())

    return jsonify(inserted_user)
