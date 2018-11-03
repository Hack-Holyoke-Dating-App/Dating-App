import os

from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

from models.user import User
from models.meme import Meme
from models.message import Message
from models.meme_rating import Meme_Rating
from models.conversation import Coversation

import libmemes

app = Flask(__name__)

# Load configuration
app.config['MONGO_URI'] = os.environ['MONGO_URI']

# Setup MongoDB
mongo = PyMongo(app)

# Insert memes if they don't exist
if mongo.db.memes.count_documents({}) == 0:
    meme_models = libmemes.make_meme_models()

    for meme_model in meme_models:
        mongo.db.memes.insert(meme_model.to_dict())
        print("Inserted meme: {}".format(meme_model.image_path))
else:
    print("Memes already inserted")

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
    
@app.route("/api/memes/<meme_id>", methods=['POST'])
def rate_meme(meme_id):
    req_meme_rating = request.json['meme_rating']

    meme_rating = Meme_Rating(id=None,
                              meme_id=ObjectId(meme_id),
                              user_id=req_meme_rating['user_id'],
                              liked=req_meme_rating['liked'])

    meme_rating_id = mongo.db.meme_ratings.insert(meme_rating.to_dict())

    meme_rating.id = str(meme_rating_id)

    return jsonify(meme_rating.to_dict())

@app.route("/api/conversations", methods=['POST'])
def create_conversation():
    req_conversation = request.json['conversation']

    conversation = Coversation(id=None,
                                user_a_id=ObjectId(req_conversation['user_a_id']),
                                user_b_id=ObjectId(req_conversation['user_b_id']))

    conversation_id = mongo.db.conversations.insert(conversation.to_dict())

    conversation.id = str(conversation_id)
    conversation.user_a_id = str(conversation.user_a_id)
    conversation.user_b_id = str(conversation.user_b_id)

    return jsonify(conversation.to_dict())
