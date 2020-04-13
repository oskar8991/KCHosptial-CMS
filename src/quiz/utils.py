from models import Questions, Answers

def get_questions(content_id):
    quiz_questions = []
    questions = Questions.query.filter_by(content_id = content_id).all()
    for q in questions:
        answers = Answers.query.filter_by(question_id = q.id).all()
        correct_answer = Answers.query.filter_by(question_id = q.id, correct = 1).first()
        correct_index = answers.index(correct_answer) if correct_answer else -1

        quiz_questions.append({
            'q': q.question_text,
            'options': [a.answer_text for a in answers],
            'correctIndex': correct_index,
            'correctResponse': 'Good job !',
            'incorrectResponse': 'That\'s the wrong answer.',
            'question_id': q.id
        })

    return quiz_questions