from flask_login import UserMixin
class User(UserMixin):
        def __init__(self, id, login, email):
            self.id = id
            self.login = login
            self.email = email

        def get_id(self):
            return self.id