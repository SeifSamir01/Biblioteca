# session.py
class Session:
    def __init__(self):
        self.user = None

    def set_user(self, username):
        self.user = username

    def get_user(self):
        return self.user
