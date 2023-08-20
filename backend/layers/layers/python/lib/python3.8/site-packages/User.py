import uuid

class User:
    def __init__(self, name, email, password, age, gender, location, user_id=None, phone_number=None):
        self.name = name
        self.email = email
        self.password = password
        self.age = age
        self.gender = gender
        self.location = location
        self.user_id = user_id or str(uuid.uuid4())
        self.phone_number = phone_number

    def to_dynamo_item(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'password': self.password,  # Ideally, passwords should be hashed!
            'age': self.age,
            'gender': self.gender,
            'location': self.location,
            'phone_number': self.phone_number
        }