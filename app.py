import os
import operator

from flask import Flask, request, jsonify, send_from_directory
from flask_pymongo import PyMongo
from flask_socketio import SocketIO

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

    return jsonify({
        'user': user.to_dict()
    })

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

    return jsonify({
        'user': user.to_dict()
    })

@app.route("/api/users/<user_id>/matches", methods=['GET'])
def get_matches(user_id):
    # Get meme ids so order of meme vectors is always the same
    db_memes = mongo.db.memes.find({})

    memes = []

    for db_meme in db_memes:
        meme = Meme(id=db_meme['_id'],
                    image_path=db_meme['image_path'])
        memes.append(meme)

    # See if more than 2 users
    if mongo.db.users.count_documents({}) < 2:
        return jsonify({
            'users': []
        })

    # Get all users
    db_users = mongo.db.users.find({})

    users = {}

    for db_user in db_users:
        user = User(id=db_user['_id'],
                    username=db_user['username'],
                    name=db_user['name'],
                    profile_picture_path=db_user['profile_picture_path'],
                    age=db_user['age'],
                    location=db_user['location'])
        users[str(user.id)] = user

    meme_vectors = {}

    # Make a meme rating vector each user
    for this_user_id in list(users):
        user = users[this_user_id]

        meme_vector = []

        # Get meme rating for each meme for user
        for meme in memes:
            # Find meme rating for user 
            meme_rating = mongo.db.meme_ratings.find_one({
                'user_id': user.id,
                'meme_id': meme.id
            })

            if meme_rating is None:
                meme_vector.append(0)
            else:
                val = 0

                if meme_rating['liked']:
                    val = 1

                meme_vector.append(val)

        meme_vectors[str(user.id)] = meme_vector

    # Find the difference between each user and requesting user
    meme_differences = {}

    for other_user_id in meme_vectors:
        # Don't compute difference for requesting user
        if user_id == other_user_id:
            continue

        # Otherwise compute difference
        similar_total = 0
        for this_user_meme_vector_slot in meme_vectors[user_id]:
            for other_user_meme_vector_slot in meme_vectors[other_user_id]:
                if this_user_meme_vector_slot == other_user_meme_vector_slot:
                    similar_total += 1

        meme_differences[other_user_id] = similar_total

    sorted_meme_differences = sorted(meme_differences.items(), key=operator.itemgetter(1))

    matched_users = []

    for tup in sorted_meme_differences:
        tup_user_id = tup[0]

        user = users[tup_user_id]
        user.id = str(user.id)

        matched_users.append(user.to_dict())


    return jsonify({
        'users': matched_users
    })


@app.route("/api/memes", methods=['GET'])
def get_memes():
    db_memes = mongo.db.memes.find({})
    all_memes = []

    for db_meme in db_memes:
        meme = Meme(id=db_meme['_id'],
                    image_path=db_meme['image_path'])
        meme.id = str(meme.id)
        all_memes.append(meme.to_dict())

    return jsonify({
        'memes': all_memes
    })


@app.route("/api/memes/<meme_id>", methods=['POST'])
def rate_meme(meme_id):
    req_meme_rating = request.json['meme_rating']

    meme_rating = Meme_Rating(id=None,
                              meme_id=ObjectId(meme_id),
                              user_id=req_meme_rating['user_id'],
                              liked=req_meme_rating['liked'])

    meme_rating_id = mongo.db.meme_ratings.insert(meme_rating.to_dict())

    meme_rating.id = str(meme_rating_id)

    return jsonify({
        'meme_rating': meme_rating.to_dict()
    })

@app.route("/api/conversations", methods=['POST'])
def create_conversation():
    # Insert into DB
    req_conversation = request.json['conversation']

    conversation = Coversation(id=None,
                                user_a_id=ObjectId(req_conversation['user_a_id']),
                                user_b_id=ObjectId(req_conversation['user_b_id']))

    conversation_id = mongo.db.conversations.insert(conversation.to_dict())

    conversation.id = str(conversation_id)
    conversation.user_a_id = str(conversation.user_a_id)
    conversation.user_b_id = str(conversation.user_b_id)

    # Notify via Socket
    for user_id in [conversation.user_a_id, conversation.user_b_id]:
        SocketIO.emit("/users/{}/new_conversations".format(user_id),
                      { 'conversation': conversation.to_dict() },
                      broadcast=True)

    return jsonify({
        'conversation': conversation.to_dict()
    })

@app.route("/api/conversations/<conversation_id>/messages", methods=['POST'])
def send_message(conversation_id):
    # Insert into DB
    req_message = request.json['message']

    message = Message(id=None,
                      conversation_id=conversation_id,
                      sending_user_id=req_message['sending_user_id'],
                      time=req_message['time'],
                      text=req_message['text'])

    message_id = mongo.db.messages.insert(message)
    message.id = str(message_id)
    message.sending_user_id = str(message.sending_user_id)

    # Notify via websocket
    SocketIO.emit("/conversations/{}/new_message".format(conversation_id),
                  { 'message': message.to_dict() },
                  broadcast=True)

@app.route("/api/conversations/<conversation_id>/messages", methods=['GET'])
def get_messages(conversation_id):
    db_messages = mongo.db.messages.find({
        'conversation_id': ObjectId(conversation_id)
    }).sort('time', PyMongo.ASCENDING)

    all_messages = []

    for db_message in db_messages:
        message = Message(id=db_message['_id'],
                          conversation_id=db_message['conversation_id'],
                          sending_user_id=db_message['sending_user_id'],
                          time=db_message['time'],
                          text=db_message['text'])

        message.id = str(message.id)
        message.conversation_id = str(message.conversation_id)
        message.sending_user_id = str(message.sending_user_id)

        all_messages.append(message.to_dict())

    return jsonify({
        'messages': all_messages
    })

@app.route("/dir/<path:path>", methods=['GET'])
def get_static_file(path):
    
    static_file_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)))
    
    # if file doesn't exist
    if not os.path.isfile(os.path.join(static_file_directory, path)):
        path = os.path.join(path, None)
        
    return send_from_directory(static_file_directory, path)
