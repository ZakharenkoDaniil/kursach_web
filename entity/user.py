class User:
    def __init__(self, id=None, login=None, password_hash=None):
        self.id = id
        self.login = login
        self.password_hash = password_hash

    def get_user_by_login(self, connection):
        cursor = connection.cursor()
        cursor.execute('''SELECT * FROM users WHERE login='{}';'''.format(self.login))
        user_data = cursor.fetchall()
        self.id = user_data[0][0]
        self.password_hash = user_data[0][2]
