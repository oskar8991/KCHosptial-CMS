from flask import render_template, Blueprint, request, redirect, url_for
from flask_login import login_required
from app import db
from models import Questions, Answers, Content
from quiz.forms import QuestionForm
from content.utils import get_by_title

quiz = Blueprint('quiz', __name__)

@quiz.route("/questions/add", methods=['GET', 'POST'])
@login_required
def add_question():
    form = QuestionForm()
    form.content.choices = [(r.page_id, r.title) for r in Content.query.all()]

    if form.validate_on_submit():
        question = Questions(question_text = form.question.data, content = Content.query.filter_by(page_id = form.content.data).first())
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

@quiz.route("/questions/delete/<question_id>")
@login_required
def delete_question(question_id):
    question = Questions.query.get(question_id)
    if question:
        db.session.delete(question)
        db.session.commit()

    return redirect(url_for('quiz.questions'))

#Update content table with input from edit.html
@quiz.route("/questions/edit/<question_id>", methods=['GET', 'POST'])
@login_required
def edit_question(question_id):
    question = Questions.query.get(question_id)
    answers = Answers.query.filter_by(question_id = question.id)
    wrong_answers = answers.filter_by(correct = 0).all()
    correct_answer = answers.filter_by(correct = 1).first()

    values = {
        'question': question.question_text,
        'wrong_answers': [a.answer_text for a in wrong_answers],
        'correct_answer': correct_answer.answer_text
    }

    form = QuestionForm(content = question.content_id)
    form.content.choices = [(r.page_id, r.title) for r in Content.query.all()]
    form.new_question = False

    if form.validate_on_submit():
        question.question_text = form.question.data
        question.content = Content.query.filter_by(page_id = form.content.data).first()
        wrong_answers[0].answer_text = form.first_answer.data
        wrong_answers[1].answer_text = form.second_answer.data
        wrong_answers[2].answer_text = form.third_answer.data
        correct_answer.answer_text = form.correct_answer.data
        db.session.commit()

        return redirect(url_for('quiz.questions'))

    return render_template('questions/edit.html', values=values, form=form)

@quiz.route("/questions")
@login_required
def questions():
    questions = Questions.query.all()

    return render_template('questions/quiz.html', questions = questions)

@quiz.route('/_answered_question')
def answered_question():
    question_id = request.args.get('question_id', -1, type=int)
    answer = request.args.get('answer', -1, type=int)

    question = Questions.query.get(question_id)
    if not question or answer == -1:
        return

    if answer:
        question.stat_right = question.stat_right + 1
    else:
        question.stat_wrong = question.stat_wrong + 1
    db.session.commit()

    return "Nothing"

@quiz.route("/dashboard/quiz-statistics")
@login_required
def quiz_statistics():
    data = Questions.query.all()

    return render_template('dashboard/quiz_statistics.html', questions=data)