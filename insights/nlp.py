# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

from bson.objectid import ObjectId

from models.conversation_analysis import ConversationAnalysis

class TextAnalysis:
    client = language.LanguageServiceClient()
    mongo = None

    def __init__(self, mongo):
        self.mongo = mongo

    def analyse(self, conversation_id):
        # Get conversation analysis model
        db_conversation_analysis = mongo.db.conversation_analysis.find_one({
            'conversation_id': ObjectId(conversation_id)
        })

        conversation_analysis = ConversationAnalysis.from_db_document(db_conversation_analysis)

        # Setup the GAPI NLP request
        document = types.Document(
            content=TBD,
            type=enums.Document.Type.PLAIN_TEXT)


def analysis(conversation):
    try:
        client = language.LanguageServiceClient()
        document = types.Document(
            content=conversation,
            type=enums.Document.Type.PLAIN_TEXT)
        sentiment = client.analyze_sentiment(document=document).document_sentiment
        categories = client.classify_text(document).categories
        #entities = client.analyze_entities(document).entities
    except:
        return

    chat = create_conversation()
    chat['score'], chat['magnitude'] = sentiment.score, sentiment.magnitude

    #entity_type = {'UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
     #              'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER'}

    """for entity in entities:
        print('=' * 20)
        print(u'{:<16}: {}'.format('name', entity.name))
        #print(u'{:<16}: {}'.format('type', entity_type[entity.type]))
        print(u'{:<16}: {}'.format('metadata', entity.metadata))
        print(u'{:<16}: {}'.format('salience', entity.salience))
        print(u'{:<16}: {}'.format('wikipedia_url',
                                   entity.metadata.get('wikipedia_url', '-')))

    for category in categories:
        print(u'=' * 20)
        print(u'{:<16}: {}'.format('name', category.name))
        print(u'{:<16}: {}'.format('confidence', category.confidence))
"""
    for category in categories:
        chat['categories'] += category.name
    return success


def get_message_accumulator():
    #Get message
    return file


def concatenate_message(file):
    #Add previous
    file += get_message_accumulator()
    return file


def create_conversation():
    conversation = {
        'score': 0,
        'magnitude': 0,
        'categories': '',
    }
    return conversation


while analysis(file) == 0:
    file = concatenate_message(file)

for x in chat:
    print(x)






