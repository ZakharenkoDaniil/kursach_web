import sqlite3

db_path = "C://Users//zakha//PycharmProjects//kursach_web//resource//sql.db"


def get_connection():
    return sqlite3.connect(db_path)


def create_tables():
    conn = get_connection()
    sql_create_users_table = '''CREATE TABLE IF NOT EXISTS users(
    id NUMBER PRIMARY KEY,
    login TEXT NOT NULL,
    password_hash TEXT NOT NULL);'''
    sql_create_words_table = '''CREATE TABLE IF NOT EXISTS words(
    id NUMBER PRIMARY KEY,
    word TEXT NOT NULL);'''
    sql_create_attempts_table = '''CREATE TABLE IF NOT EXISTS attempts(
    user_id NUMBER,
    word_id NUMBER,
    attempt_number NUMBER);'''
    cursor = conn.cursor()
    cursor.execute(sql_create_users_table)
    cursor.execute(sql_create_words_table)
    cursor.execute(sql_create_attempts_table)
    conn.commit()
    cursor.close()
    conn.close()


def fill_words():
    conn = get_connection()
    cursor = conn.cursor()
    sql_fill_word_table = '''INSERT INTO words VALUES('{}','{}')'''
    words = [
        'слово',
        'игра'
    ]
    id = 1
    for word in words:
        cursor.execute(sql_fill_word_table.format(id, word))
        id += 1
    conn.commit()
    cursor.close()
    conn.close()