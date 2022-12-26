from random import randint


def get_random_word_from_db(connection):
    cursor = connection.cursor()
    cursor.execute('''SELECT COUNT(*) FROM words''')
    max_id = cursor.fetchone()[0]
    id = randint(1, max_id)
    cursor.execute('''SELECT word FROM words WHERE id={}'''.format(id))
    word = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()
    return Word(id, word)


class Word:
    def __init__(self, id=None, word=None):
        self.id = id
        self.word = word
