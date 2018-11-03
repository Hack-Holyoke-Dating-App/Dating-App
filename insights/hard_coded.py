from bson.objectid import ObjectId

from models.message import Message
from models.conversation_analysis import ConversationAnalysis
from models.conversation import Conversation
from models.user_topics import User_Topics

from .send_insight import send_insight

INSIGHT_OPENER = 'opener'
INSIGHT_DATE = 'date'
INSIGHT_RATIO = 'ratio'
INSIGHT_TOPIC = 'topic'

class HardCodedAnalysis:
    mongo = None
    socketio = None

    def __init__(self, mongo, socketio):
        self.mongo = mongo
        self.socketio = socketio

    def analyse(self, conversation_id, last_message_sender_id):
        conversation_query = { 'conversation_id': ObjectId(conversation_id) }

        # Get conversation analysis
        db_conversation_analysis = self.mongo.db.conversation_analysis.find_one(conversation_query)
        conversation_analysis = ConversationAnalysis.from_db_document(db_conversation_analysis)

        # Get conversation
        db_conversation = self.mongo.db.conversations.find_one({ '_id': ObjectId(conversation_id) })
        conversation = Conversation.from_db_document(db_conversation)

        # Determine if last message sender is a or b
        last_message_sender_letter = 'a'
        other_letter = 'b'

        if last_message_sender_id == str(conversation.user_b_id):
            last_message_sender_letter = 'b'
            other_letter = 'a'

        # Get other user id
        other_user_id = str(conversation.user_a_id)

        if other_user_id == last_message_sender_id:
            other_user_id = str(conversation.user_b_id)

        # Get sentiments
        last_message_sender_sentiment = conversation_analysis.sentiment_a
        other_user_sentiment = conversation_analysis.sentiment_b

        if last_message_sender_id == str(conversation.user_b_id):
            last_message_sender_sentiment = conversation_analysis.sentiment_b
            other_user_sentiment = conversation_analysis.sentiment_a

        conversation_message_count = self.mongo.db.messages.count_documents(conversation_query)

        # Boring intro
        if conversation_message_count == 1:
            db_message = mongo.db.messages.find_one(conversation_query)
            message = Message.from_db_document(db_message)

            if len(message.text) < 10:
                send_insight(self.socketio,
                             conversation_id,
                             str(message.sending_user_id),
                             INSIGHT_OPENER,
                             "Try starting with a more interesting message")

        # Ask them out
        if ("{}.{}".format(last_message_sender_letter, INSIGHT_DATE) not in conversation_analysis.sent_insights) and \
                last_message_sender_sentiment >= 0.3:
            send_insight(self.socketio,
                         conversation_id,
                         other_user_id,
                         INSIGHT_DATE,
                         "It seams like your match is into your, try asking them out on a date!")

            conversation_analysis.sent_insights.append("{}.{}".format(last_message_sender_letter, INSIGHT_DATE))

        # Message ratio
        if conversation_message_count > 5:
            # Get message counts
            last_sender_msg_count = self.mongo.db.messages.count_documents({
                'conversation_id': ObjectId(conversation_id),
                'sending_user_id': ObjectId(last_message_sender_id)
            })
            other_msg_count = self.mongo.db.messages.count_documents({
                'conversation_id': ObjectId(conversation_id),
                'sending_user_id': ObjectId(other_user_id)
            })

            # Compute ratios
            last_sender_ratio = last_sender_msg_count / other_msg_count
            other_ratio = other_msg_count / last_sender_msg_count

            # Determine if ratios are bad
            ratio_user_ids = []

            if ("{}.{}".format(last_message_sender_letter, INSIGHT_RATIO) not in conversation_analysis.sent_insights) and \
                    last_sender_ratio > 2.5:

                ratio_user_ids.append(ObjectId(last_message_sender_id))

            if ("{}.{}".format(other_letter, INSIGHT_RATIO) not in conversation_analysis.sent_insights) and \
                    other_ratio > 2.5:

                ratio_user_ids.append(ObjectId(other_user_id))

            # Send insights
            for user_id in ratio_user_ids:
                send_insight(self.socketio,
                             conversation_id,
                             str(user_id),
                             INSIGHT_RATIO,
                             "Looks like you are sending a lot of messages, try toning it down")

        # Topic change
        if ("{}.{}".format(other_letter, INSIGHT_TOPIC)) and \
                other_user_sentiment < -0.2:

            db_other_user_topics = self.mongo.db.user_topics.find_one({ 'user_id': ObjectId(other_user_id) })
            other_user_topics = User_Topics.from_db_document(db_other_user_topics)

            msg = "It doesn't look like your match is interested, try talking about {}".format(", ".join(other_user_topics.topics))

            send_insight(self.socketio,
                         conversation_id,
                         other_user_id,
                         INSIGHT_TOPIC,
                         msg)
