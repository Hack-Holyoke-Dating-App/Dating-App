# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

from bson.objectid import ObjectId

from models.conversation_analysis import ConversationAnalysis
from models.conversation import Conversation
from models.user_topics import User_Topics

class TextAnalysis:
    client = language.LanguageServiceClient()
    mongo = None

    def __init__(self, mongo):
        self.mongo = mongo

    def analyse(self, conversation_id):
        # Get conversation analysis model
        db_conversation_analysis = self.mongo.db.conversation_analysis.find_one({
            'conversation_id': ObjectId(conversation_id)
        })

        conversation_analysis = ConversationAnalysis.from_db_document(db_conversation_analysis)

        # Get conversation
        db_conversation = self.mongo.db.conversations.find_one({ '_id': ObjectId(conversation_id) })

        conversation = Conversation.from_db_document(db_conversation)

        # Get user topics for each user
        # ... User a
        db_user_a_topics = self.mongo.db.user_topics.find_one({ 'user_id': conversation.user_a_id })
        user_a_topics = User_Topics.from_db_document(db_user_a_topics)

        # ... User b
        db_user_b_topics = self.mongo.db.user_topics.find_one({ 'user_id': conversation.user_b_id })
        user_b_topics = User_Topics.from_db_document(db_user_b_topics)

        # Setup the GAPI NLP request
        # ... Make one for entire conversation
        both_text = "{} {}".format(conversation_analysis.text_to_analyse_a,
                                   conversation_analysis.text_to_analyse_b)

        document_both = types.Document(
            content=both_text,
            type=enums.Document.Type.PLAIN_TEXT)

        # ... Make one request for user a's text
        document_a = types.Document(
            content=conversation_analysis.text_to_analyse_a,
            type=enums.Document.Type.PLAIN_TEXT)

        # ... Make one request for user b's text
        document_b = types.Document(
            content=conversation_analysis.text_to_analyse_b,
            type=enums.Document.Type.PLAIN_TEXT)

        # Make sentiment call
        sentiment = self.make_sentiment_call(document_both)

        # Update conversation analysis sentiment
        conversation_analysis.sentiment = sentiment.score * sentiment.magnitude
        #conversation_analysis.sentiment_n += 1

        # Make categories calls
        user_a_categories = self.make_categories_call(document_a)
        user_b_categories = self.make_categories_call(document_b)

        if user_a_categories is not None:
            # Add new categories
            for category in user_a_categories:
                name = category.name

                if name not in user_a_topics.topics:
                    user_a_topics.topics.append(name)

            # Save topics
            self.mongo.db.user_topics.update({ '_id': user_a_topics.id },
                                             user_a_topics.to_dict())

            # Clear text to analyse a
            conversation_analysis.text_to_analyse_a = ""

        if user_b_categories is not None:
            # Add new categories
            for category in user_b_categories:
                name = category.name

                if name not in user_b_topics.topics:
                    user_b_topics.topics.append(name)

            # Save topics
            self.mongo.db.user_topics.update({ '_id': user_b_topics.id },
                                             user_b_topics.to_dict())

            # Clear text to analyse a
            conversation_analysis.text_to_analyse_b = ""

        # Update conversation analysis
        self.mongo.db.conversation_analysis.update({ '_id': conversation_analysis.id },
                                              conversation_analysis.to_dict())

    def make_sentiment_call(self, document):
        return self.client.analyze_sentiment(document=document).document_sentiment

    def make_categories_call(self, document):
        try:
            return self.client.classify_text(document).categories
        except Exception as e:
            return None
