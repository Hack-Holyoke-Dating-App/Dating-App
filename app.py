import os

from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from models.user import User

app = Flask(__name__)

# Load configuration
app.config['MONGO_URI'] = os.environ['MONGO_URI']

# Setup MongoDB
mongo = PyMongo(app)

@app.route("/api/users", methods=['POST'])
def create_user():
    req_user = request.json['user']

    user = User(id=None,
                username=req_user['username'],
                name=req_user['name'],
                profile_picture_path=None,
                age=req_user['age'],
                location=req_user['location'])

    user_id = mongo.db.users.insert(user.to_dict())

    user.id = str(user_id)

    return jsonify(user.to_dict())

@app.route("/api/users/<user_id>", methods=['GET'])
def get_user(user_id):
    db_user = mongo.db.users.find_one({'_id' :  ObjectId(user_id)})
    
    user = User(id=user_id,
                username=db_user['username'],
                name=db_user['name'],
                profile_picture_path=db_user['profile_picture_path'],
                age = db_user['age'],
                location = db_user['location']
                )
    
    return jsonify(user.to_dict())
