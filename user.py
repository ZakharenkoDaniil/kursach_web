class User:
    def __init__(self, login=None, password_hash=None):
        self.login = login
        self.password_hash = password_hash
