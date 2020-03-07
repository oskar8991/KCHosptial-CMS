 
from medications import medicationsList, generateChart
from flask import Flask, url_for, redirect, render_template, request, session, abort, flash, Response, stream_with_context
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from functools import wraps
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' #configuring database
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

engine = create_engine('sqlite:///data.db', echo = True)
meta = MetaData()
Base = declarative_base()

#Creates a table for login form with id, email and password
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)

class questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    questionText = db.Column(db.String(30), nullable=False)

class answers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answerText = db.Column(db.String(30), nullable=False)
    correct = db.Column(db.Integer(), unique=False, nullable=False)

class question_answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.id'))
    answer_id = Column(Integer, ForeignKey('answers.id'))


#Creates a table for web page content with id and text
pageContent = Table(
    'content', meta,
    Column("page_id", Integer, primary_key=True),
    Column("content", Text),
)
meta.create_all(engine)

'''
class Page(Base):
    __tablename__ = 'content'
    Column("page_id", Integer, primary_key=True)
    Column("content", Text)
'''

#Populate content table with input from add new page content
@app.route("/populateContent", methods=['POST'])
def populateContent():
    inputString = request.form['editBox']
    #INSERT INTO content (content) VALUES (inputString)
    insertStatement = pageContent.insert().values(content = inputString)
    conn = engine.connect()
    result = conn.execute(insertStatement)
    return redirect(url_for('index'))

@app.route("/populateQuestions", methods=['POST'])
def populateQuestions():
    question = request.form['question']
    answer1 = request.form['answer1']
    answer2 = request.form['answer2']
    answer3 = request.form['answer3']
    correctAnswer = request.form['correctAnswer']
    questions1 = questions(questionText = question)
    answers1 = answers(answerText = answer1, correct = 0)
    answers2 = answers(answerText = answer2, correct = 0)
    answers3 = answers(answerText = answer3, correct = 0)
    answers4 = answers(answerText = correctAnswer, correct = 1)
    db.session.add(questions1)
    db.session.commit()
    db.session.add(answers1)
    db.session.commit()
    db.session.add(answers2)
    db.session.commit()
    db.session.add(answers3)
    db.session.commit()
    db.session.add(answers4)
    db.session.commit()
    #question_answer1 = question_answer(question_id = questions1.id, answer_id = answer1.id)
    #question_answer2 = question_answer(question_id = questions1.id, answer_id = answer2.id)
    #question_answer3 = question_answer(question_id = questions1.id, answer_id = answer3.id)
    #question_answer4 = question_answer(question_id = questions1.id, answer_id = answer4.id)
    #db.session.add(question_answer1)
    #db.session.add(question_answer4, question_answer4)
    #db.session.commit()   
    return redirect(url_for('quiz'))


#Update content table with input from edit.html
@app.route("/updateContent", methods=['POST'])
def updateContent():
    inputString = request.form['editBox']
    #UPDATE first row in table content
    updateStatement = pageContent.update().where(pageContent.c.page_id==1).values(content = inputString)
    conn = engine.connect()
    result = conn.execute(updateStatement)
    return redirect(url_for('index'))


@app.route('/index')
#content table query for index.html
def retrieveContentIndex():
    # Equivalent to SELECT * FROM pageContent
    select = pageContent.select()
    conn = engine.connect()
    result = conn.execute(select)
    outputRow = result.fetchone()
    for row in result:
        if (row.page_id == 1):
            outputRow = row
    return render_template('index.html', content=outputRow.content)

@app.route('/edit')
#content table query for Edit.html
def retrieveContentEdit():
    # Equivalent to SELECT * FROM pageContent
    select = pageContent.select()
    conn = engine.connect()
    result = conn.execute(select)
    outputRow = result.fetchone()
    for row in result:
        if (row.page_id == 1):
            outputRow = row
    return render_template('edit.html', content=outputRow.content)




@app.route('/medication', methods=['GET', 'POST'])
def medication():
    if request.method == 'POST':
        selected = [med for med in medicationsList if med.name in request.form]
        return render_template('chart.html', chart=generateChart(selected))

    return render_template('medication.html', medications=medicationsList)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return render_template('index.html')



@app.route('/login')
def login():
    return render_template('auth/login.html')

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))

    return wrap

@app.route("/logmein", methods=['POST'])
def logmein():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(email = username).first()

    if not user:
        flash('Invalid credentials')
        return redirect(url_for('login'))
    else:
        if user.password != password:
            flash('Invalid credentials')
            return redirect(url_for('login'))
        else:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))



@app.route("/logout")
@login_required
def logout():
    session['logged_in'] = False
    session.clear()
    return redirect(url_for('index'))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route("/edit")
@login_required
def edit():
    return render_template('edit.html')


@app.route("/users")
@login_required
def users():
    conn = engine.connect()
    query = "SELECT id, email from user"
    result = conn.execute(query)
    data = result.fetchall()
    return render_template('users.html', data = data)


@app.route("/quiz")
@login_required
def quiz():
    conn = engine.connect()
    query = "SELECT * from questions"
    result = conn.execute(query)
    questions = result.fetchall()
    return render_template('quiz.html', questions = questions)

@app.route("/question")
@login_required
def question():
    return render_template('question.html')    


############# FOR TESTING SEARCHBAR #########
@app.route("/searchBarSample")
def searchBarSample():
    return render_template('searchBarSample.html')
#############################################

if __name__ == '__main__':
    app.secret_key = '_5#y2L"F4Q8z\n\xec]/'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run()
