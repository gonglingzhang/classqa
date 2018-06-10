# encoding:utf-8
from flask import Flask, render_template, request, redirect, url_for, session
import config
from models import User, Question, Answer
from exts import db
from decorators import login_required

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)


@app.route('/')
def index():
    context = {
        'questions': Question.query.order_by('-create_time').all()
    }
    return render_template('index.html', **context)


@app.route('/query_key/', methods=['POST'])
def query_key():
    query = request.form.get('query_key')
    query_context = {
        'query_questions': Question.query.order_by('-create_time').filter(Question.title.ilike('%'+query+'%')).all()
    }
    return render_template('query_result.html', **query_context)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone, User.password == password).first()
        if user:
            session['user_id'] = user.id
            # 31天内有效
            session.permanent = True
            return redirect(url_for('question'))
        else:
            return "用户名或密码错误！"


@app.route('/regist/', methods=['GET', 'POST'])
def regist():
    if request.method == "GET":
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return "该手机号码已经注册！"
        else:
            if password1 != password2:
                return "两次密码输入不一致，请重新输入！"
            else:
                user1 = User(telephone=telephone, username=username, password=password1)
                db.session.add(user1)
                db.session.commit()
                return redirect(url_for('login'))


@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/question/', methods=['GET', 'POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question1 = Question(title=title, content=content)  # 前台获取标题和内容
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        question1.author = user  # 使用relationship设置外键的用户
        db.session.add(question1)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/detail/<question_id>')
def detail(question_id):
    question_model = Question.query.filter(Question.id == question_id).first()
    answer_count = len(Answer.query.filter(Answer.question_id == question_id).all())
    return render_template('detail.html', question=question_model, answer_count=answer_count)


@app.route('/add_answer/', methods=['POST'])
@login_required
def add_answer():
    answer_content = request.form.get('answer_content')
    user_id = session.get('user_id')
    user1 = User.query.filter(User.id == user_id).first()
    question_id = request.form.get('question_id')
    question1 = Question.query.filter(Question.id == question_id).first()
    answer1 = Answer(content=answer_content)
    answer1.author = user1
    answer1.question = question1
    db.session.add(answer1)
    db.session.commit()
    return redirect(url_for('detail', question_id=question_id))


@app.context_processor
def my_context_processor():
    user = User.query.filter(User.id == session.get('user_id')).first()
    if user:
        return {'user': user}
    else:
        return {}


if __name__ == '__main__':
    app.run()
