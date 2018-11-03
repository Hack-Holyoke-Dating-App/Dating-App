class ConversationAnalysis:
    def __init__(self, id, conversation_id, sentiment, sentiment_n,
                 text_to_analyse_a, text_to_analyse_b):
        self.id = id
        self.conversation_id = conversation_id
        self.sentiment = sentiment
        self.sentiment_n = sentiment_n
        self.text_to_analyse_a = text_to_analyse_a
        self.text_to_analyse_b = text_to_analyse_b

    @classmethod
    def from_db_document(cls, doc):
        return ConversationAnalysis(id=doc['_id'],
                                    conversation_id=doc['conversation_id'],
                                    sentiment=doc['sentiment'],
                                    sentiment_n=doc['sentiment_n'],
                                    text_to_analyse_a=doc['text_to_analyse_a'],
                                    text_to_analyse_b=doc['text_to_analyse_b'])

    """
    def get_avrg_setiment(self):
        if self.sentiment_n == 0:
            return 0

        return self.sentiment / self.sentiment_n
    """

    def to_dict(self):
        d = {
            'conversation_id': self.conversation_id,
            'sentiment': self.sentiment,
            'sentiment_n': self.sentiment_n,
            'text_to_analyse_a': self.text_to_analyse_a,
            'text_to_analyse_b': self.text_to_analyse_b
        }

        if self.id:
            d['_id'] = self.id

        return d

    def to_str_dict(self):
        d = self.to_dict()

        d['conversation_id'] = str(d['conversation_id'])

        return d
