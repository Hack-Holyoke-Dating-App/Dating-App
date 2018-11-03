# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

#Test file
file = u'When can a center relax with the justifiable vocal? When can a center relax with the justifiable vocal? When can a center relax with the justifiable vocal? When can a center relax with the justifiable vocal? When can a center relax with the justifiable vocal? When can a center relax with the justifiable vocal?When can a center relax with the justifiable vocal? Why can\'t the league learn the crossroad? The audio dreads an undone aspect. Will a crown see the definitive specimen? Each fool reminder pats the potential company. Opposite the identical species jams a probable spy.'


def analysis(conversation):
    client = language.LanguageServiceClient()
    document = types.Document(
        content=conversation,
        type=enums.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(document=document).document_sentiment
    categories = client.classify_text(document).categories
    entities = client.analyze_entities(document).entities
    return sentiment, entities, categories


def print_results(sentiment, entities, categories):
    print(sentiment.score, sentiment.magnitude)

    #entity_type = {'UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
     #              'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER'}

    for entity in entities:
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

sentiment, entities, categories = analysis(file)
print_results(sentiment, entities, categories)




