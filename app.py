
from medications import medicationsList, generateChart
from flask import Flask, url_for, redirect, render_template, request, session, abort, flash, Response, stream_with_context
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, Boolean, ForeignKey

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

engine = create_engine('sqlite:///data.db', echo = True)
meta = MetaData()

#Creates a table for login form with id, email and password
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)

class questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    questionText = db.Column(db.String(30), nullable=False)

class answers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answerText = db.Column(db.String(30), nullable=False)
    correct = db.Column(db.Integer(), unique=False, nullable=False)

class question_answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = Column(db.Integer, ForeignKey('questions.id'))
    answer_id = Column(db.Integer, ForeignKey('answers.id'))


#Creates a table for web page content with id and text
pageContent = Table(
    'content', meta,
    Column("page_id", Integer, primary_key=True),
    Column("content", Text),
)
meta.create_all(engine)

def login_required(f):
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))

    return wrap



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
    ques = questions(questionText = request.form['question'])
    answ = [
        answers(answerText = request.form['answer1'], correct = 0),
        answers(answerText = request.form['answer2'], correct = 0),
        answers(answerText = request.form['answer3'], correct = 0),
        answers(answerText = request.form['correctAnswer'], correct = 1)
    ]

    db.session.add(ques)
    for answer in answ:
        db.session.add(answer)
        db.session.add(
            question_answer(question_id = ques.id, answer_id = answer.id)
        )

    db.session.commit()
    return redirect(url_for('quiz'))


@login_required
@app.route("/deleteQuestion/<question_id>")
def deleteQuestion(question_id):
    question = questions.query.filter_by(id = question_id).first_or_404()
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('quiz'))

@login_required
@app.route("/deleteUser/<user_id>")
def deleteUser(user_id):
    user = User.query.filter_by(id = user_id).first_or_404()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users'))


#Update content table with input from edit.html
@login_required
@app.route("/updateQuestion", methods=['POST'])
def updateQuestion():
    inputString = request.form['editBox']
    #UPDATE first row in table content
    updateStatement = pageContent.update().where(pageContent.c.page_id==1).values(content = inputString)
    conn = engine.connect()
    result = conn.execute(updateStatement)
    return redirect(url_for('index'))


#Update content table with input from edit.html
@login_required
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

@login_required
@app.route('/editQuestion')
def editQuestion(question_id):
    conn = engine.connect()
    query = "SELECT * from questions WHERE id = question_id"
    result = conn.execute(query)
    question = result.fetchall()
    return render_template('editQuestion.html', question = question)



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



@app.route("/logmein", methods=['POST'])
def logmein():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(email = username).first()

    if not user or user.password != password:
        flash('Invalid credentials')
        return redirect(url_for('login'))
    else:
        session['logged_in'] = True
        return redirect(url_for('dashboard'))



@login_required
@app.route("/logout")
def logout():
    session['logged_in'] = False
    session.clear()
    return redirect(url_for('index'))


@login_required
@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

@login_required
@app.route("/edit")
def edit():
    return render_template('edit.html')


@login_required
@app.route("/users")
def users():
    conn = engine.connect()
    query = "SELECT id, email from user"
    result = conn.execute(query)
    data = result.fetchall()
    return render_template('users.html', data = data)


@login_required
@app.route("/quiz")
def quiz():
    conn = engine.connect()
    query = "SELECT * from questions"
    result = conn.execute(query)
    questions = result.fetchall()
    return render_template('quiz.html', questions = questions)

@login_required
@app.route("/question")
def question():
    return render_template('question.html')   


@login_required
@app.route("/addUser")
def addUser():
    return render_template('addUser.html')

@app.route("/addContentUser", methods=['POST'])
def addContentUser():
    userEmail = request.form['userEmail']
    userPassword = request.form['userPassword']
    user = User(email = userEmail, password = userPassword)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('users'))


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
