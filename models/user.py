class User:
    def __init__(self, id, username, name, profile_picture_path, age, location):
        self.id = id
        self.username = username
        self.name = name
        self.profile_picture_path = profile_picture_path
        self.age = age
        self.location = location

    @classmethod
    def from_db_document(cls, doc):
        return User(id=doc['_id'],
                    username=doc['username'],
                    name=doc['name'],
                    profile_picture_path=doc['profile_picture_path'],
                    age=doc['age'],
                    location=doc['location'])

    def to_dict(self):
        d = {
                'username' : self.username,
                'name': self.name,
                'profile_picture_path' : self.profile_picture_path,
                'age' : self.age,
                'location' : self.location
                }

        if self.id:
            d['_id'] = self.id

        return d

    def to_str_dict(self):
        d = self.to_dict()

        if self.id:
            d['_id'] = str(self.id)

        return d
