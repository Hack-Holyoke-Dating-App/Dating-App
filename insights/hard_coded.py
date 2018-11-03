from bson.objectid import ObjectId

from models.message import Message

from .send_insight import send_insight

class HardCodedAnalysis:
    mongo = None
    socketio = None

    def __init__(self, mongo, socketio):
        self.mongo = mongo
        self.socketio = socketio

    def analyse(self, conversation_id):
        conversation_query = { 'conversation_id': ObjectId(conversation_id) }
        conversation_message_count = self.mongo.db.messages.count_documents(conversation_query)
        # Boring intro
        if conversation_message_count == 1:
            db_message = mongo.db.messages.find_one(conversation_query)
            message = Message.from_db_document(db_message)

            if len(message.text) < 10:
                send_insight(self.socketio,
                             conversation_id,
                             str(message.sending_user_id),
                             'opener',
                             "Try starting with a more interesting message")

        # Ask them out

