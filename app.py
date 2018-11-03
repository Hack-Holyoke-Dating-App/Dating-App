import os

from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from models.user import User
from models.meme import Meme
from models.message import Message

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

@app.route("/api/memes", methods=['GET'])
def get_memes():
    db_memes = mongo.db.memes.find({})
    all_memes = []
    
    for db_meme in db_memes:
        meme = Meme(id=db_meme['_id'])
        meme.id = str(meme.id)
        all_memes.append(meme.to_dict())
        
    return jsonify(all_memes)
    
@app.route("/api/conversations/<conversation_id>/messages", methods=['GET'])
def get_messages():
    db_messages = mongo.db.messages.find({})
    all_messages = []
    
    for db_message in db_messages:
        message = Message(id=db_message['_id'])
        message.id = str(message.id)
        all_messages.append(message.to_dict())
        
    print(all_messages)
    