class ConversationAnalysis:
    def __init__(self, id, conversation_id, sentiment_a, sentiment_b,
                 text_to_analyse_a, text_to_analyse_b, sent_insights):
        self.id = id
        self.conversation_id = conversation_id
        self.sentiment_a = sentiment_a
        self.sentiment_b = sentiment_b
        self.text_to_analyse_a = text_to_analyse_a
        self.text_to_analyse_b = text_to_analyse_b
        self.sent_insights = sent_insights

    @classmethod
    def from_db_document(cls, doc):
        return ConversationAnalysis(id=doc['_id'],
                                    conversation_id=doc['conversation_id'],
                                    sentiment_a=doc['sentiment_a'],
                                    sentiment_b=doc['sentiment_b'],
                                    text_to_analyse_a=doc['text_to_analyse_a'],
                                    text_to_analyse_b=doc['text_to_analyse_b'],
                                    sent_insights=doc['sent_insights'])

    def to_dict(self):
        d = {
            'conversation_id': self.conversation_id,
            'sentiment_a': self.sentiment_a,
            'sentiment_b': self.sentiment_b,
            'text_to_analyse_a': self.text_to_analyse_a,
            'text_to_analyse_b': self.text_to_analyse_b,
            'sent_insights': self.sent_insights
        }

        if self.id:
            d['_id'] = self.id

        return d

    def to_str_dict(self):
        d = self.to_dict()

        d['conversation_id'] = str(d['conversation_id'])

        if self.id:
            d['_id'] = str(self.id)

        return d
