import sqlite3

from flask import Flask, request, render_template, redirect

db_path = "C://Users//zakha//PycharmProjects//kursach_web//resource//sql.db"

conn = sqlite3.connect(db_path)
sql_create = '''CREATE TABLE IF NOT EXISTS users(
id NUMBER PRIMARY KEY,
login TEXT NOT NULL,
password_hash TEXT NOT NULL);'''
cursor = conn.cursor()
cursor.execute(sql_create)
conn.commit()
cursor.close()
conn.close()

app = Flask(__name__)


@app.route('/authorization', methods=['GET', 'POST'])
def form_authorization():
    if request.method == 'POST':
        login = request.form.get('Login')
        password = request.form.get('Password')
        db_lp = sqlite3.connect(db_path)
        cursor_db = db_lp.cursor()
        cursor_db.execute(('''SELECT password_hash FROM users
                                               WHERE login = '{}';
                                               ''').format(login))
        pas = cursor_db.fetchall()
        cursor_db.close()
        try:
            if pas[0][0] != password:
                return redirect('/bad_authorization')
        except:
            return redirect('/bad_authorization')

        db_lp.close()
        return redirect('/menu')

    return render_template('authorization.html')


@app.route('/bad_authorization', methods=['GET', 'POST'])
def form_bad_authorization():
    if request.method == 'GET':
        return render_template('auth_bad.html')
    else:
        return redirect('/authorization')


@app.route('/menu', methods=['GET', 'POST'])
def form_menu():
    if request.method == 'POST':
        print(request.json())
        return render_template('menu.html')
    else:
        return render_template('menu.html')


@app.route('/registration', methods=['GET', 'POST'])
def form_registration():
    if request.method == 'POST':
        login = request.form.get('Login')
        password = request.form.get('Password')

        db_lp = sqlite3.connect(db_path)
        cursor_db = db_lp.cursor()
        cursor_db.execute('''SELECT COUNT(*) FROM users''')
        count = cursor_db.fetchall()
        sql_insert = '''INSERT INTO users VALUES('{}','{}','{}');'''.format(count, login, password)

        cursor_db.execute(sql_insert)
        db_lp.commit()

        cursor_db.close()
        db_lp.close()

        return render_template('successfulregister.html')

    return render_template('registration.html')
