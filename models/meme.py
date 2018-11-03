
class Meme:
    def __init__(self, id, image_path):
        self.id = id
        self.image_path = image_path

    def to_dict(self):
        d = {
            'image_path': self.image_path
        }

        if (self.id):
            d['_id'] = self.id

        return d
