class Statistic:
    def __init__(self, user_id):
        self.user_id = user_id
        self.words = None
        self.attempts = None

    def get_statistic_for_user(self, connection):
        self.words = []
        self.attempts = []
        cursor = connection.cursor()
        cursor.execute('''SELECT * FROM attempts WHERE user_id='{}';'''.format(self.user_id))
        stat_data = cursor.fetchall()
        for data in stat_data:
            cursor.execute('''SELECT word FROM words WHERE id='{}';'''.format(data[1]))
            word = cursor.fetchone()
            self.words.append(word)
            self.attempts.append(data[2]+1)
        connection.commit()
        cursor.close()
        connection.close()
