from flask import render_template, Blueprint, request, redirect, url_for
from flask_login import login_required
from app import db
from models import Questions, Answers
from quiz.forms import AddQuestion

quiz = Blueprint('quiz', __name__)

@login_required
@quiz.route("/questions/add", methods=['GET', 'POST'])
def add_question():
    form = AddQuestion()

    if form.validate_on_submit():
        question = Questions(question_text = form.question.data)
        answers = [
            Answers(answer_text = form.first_answer.data, correct = 0, question = question),
            Answers(answer_text = form.second_answer.data, correct = 0, question = question),
            Answers(answer_text = form.third_answer.data, correct = 0, question = question),
            Answers(answer_text = form.correct_answer.data, correct = 1, question = question)
        ]

        db.session.add(question)
        for answer in answers:
            db.session.add(answer)

        db.session.commit()
        return redirect(url_for('quiz.questions'))

    return render_template('questions/add.html', form=form)

@login_required
@quiz.route("/questions/delete/<question_id>")
def delete_question(question_id):
    question = Questions.query.get(question_id)
    if question:
        db.session.delete(question)
        db.session.commit()

    return redirect(url_for('quiz.questions'))

#Update content table with input from edit.html
@login_required
@quiz.route("/questions/edit/<question_id>", methods=['GET', 'POST'])
def edit_question(question_id):
    question = Questions.query.get(question_id)

    if request.method == 'POST':
        if question:
            question.question_text = request.form['question']
            answers = Answers.query.filter(question = question).all()
            db.session.commit()

        return redirect(url_for('quiz.questions'))

    return render_template('questions/edit.html', question = question)

@login_required
@quiz.route("/questions")
def questions():
    questions = Questions.query.all()

    return render_template('questions/quiz.html', questions = questions)