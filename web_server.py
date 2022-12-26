from flask import Flask, request, render_template, redirect

from context import Context
from entity.statistic import Statistic
from entity.user import User
from entity.word import Word, get_random_word_from_db
from game import check_word
from utils.db_utils import get_connection

context = Context()
app = Flask(__name__)


@app.route('/authorization', methods=['GET', 'POST'])
def form_authorization():
    if request.method == 'POST':
        login_from_form = request.form.get('Login')
        password = request.form.get('Password')
        db_lp = get_connection()
        cursor_db = db_lp.cursor()
        cursor_db.execute('''SELECT password_hash FROM users WHERE login='{}';'''.format(login_from_form))
        pas = cursor_db.fetchall()
        cursor_db.close()
        try:
            if pas[0][0] != password:
                return redirect('/bad_authorization')
        except:
            return redirect('/bad_authorization')
        db_lp.close()
        user = User(None, login_from_form, password)
        user.get_user_by_login(get_connection())
        context.user = user
        return redirect('/menu')

    return render_template('authorization.html')


@app.route('/bad_authorization', methods=['GET', 'POST'])
def form_bad_authorization():
    if request.method == 'GET':
        return render_template('auth_bad.html')
    else:
        return redirect('/authorization')


@app.route('/registration', methods=['GET', 'POST'])
def form_registration():
    if request.method == 'POST':
        login = request.form.get('Login')
        password = request.form.get('Password')
        db_lp = get_connection()
        cursor_db = db_lp.cursor()
        cursor_db.execute('''SELECT COUNT(*) FROM users''')
        count = cursor_db.fetchall()
        sql_insert = '''INSERT INTO users VALUES('{}','{}','{}');'''.format(count[0][0], login, password)
        cursor_db.execute(sql_insert)
        db_lp.commit()
        cursor_db.close()
        db_lp.close()
        return render_template('successfulregister.html')
    return render_template('registration.html')


@app.route('/menu', methods=['GET', 'POST'])
def form_menu():
    if request.method == 'GET':
        if not len(request.args) == 0:
            if request.args.get('new') is not None:
                return redirect('/game')
            elif request.args.get('statistic') is not None:
                return redirect('/statistic')
        return render_template('menu.html')
    else:
        return render_template('menu.html')


@app.route('/new', methods=['GET', 'POST'])
def new_game():
    if request.method == 'POST':
        return 'POST'
    return redirect('/game')


@app.route('/game', methods=['GET', 'POST'])
def game():
    if request.method == 'POST':
        word_from_form = request.form.get('Word')
        result = check_word(context.word.word, word_from_form)
        if result == 'Угадано':
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute('''INSERT INTO attempts VALUES('{}','{}','{}')'''.format(context.user.id,
                                                                                    context.word.id,
                                                                                    context.attempts))
            connection.commit()
            cursor.close()
            connection.close()
            return redirect('/menu')
        return render_template('game_with_message.html', result=result)
    else:
        word = get_random_word_from_db(get_connection())
        context.word = word
        return render_template('game.html')


@app.route('/statistic', methods=['GET', 'POST'])
def statistic():
    if request.method == 'POST':
        return redirect('/menu')
    user = context.user
    stat = Statistic(user.id)
    stat.get_statistic_for_user(get_connection())
    result = ''
    for word, attempts in zip(stat.words, stat.attempts):
        result += 'Слово {} угадано с {} попытки\n'.format(word, attempts)
    return render_template('statistic_info.html', result=result)
