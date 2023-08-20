class Match:
    def __init__(self, user_id, liked_user_id, status='liked'):
        self.user_id = user_id
        self.liked_user_id = liked_user_id
        self.status = status

    def to_dynamo_item(self):
        return {
            'user_id': self.user_id,
            'liked_user_id': self.liked_user_id,
            'status': self.status
        }
