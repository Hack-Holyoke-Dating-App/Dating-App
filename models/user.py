class User:
    def __init__(self, id, username, name, profile_picture_path, age, location):
        self.id = id
        self.username = username
        self.name = name
        self.profile_picture_path = profile_picture_path
        self.age = age
        self.location = location
        
    def to_dict(self):
        return {
                'id' : self.id,
                'username' : self.username,
                'name': self.name,
                'profile_picture_path' : self.profile_picture_path,
                'age' : self.age,
                'location' : self.location
                }
