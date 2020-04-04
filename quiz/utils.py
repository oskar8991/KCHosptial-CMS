from models import Questions, Answers

def get_questions(content_id):
    quiz_questions = []
    for q in Questions.query.filter_by(content_id = content_id).all():
        answers = Answers.query.filter_by(question_id = q.id)
        correct_answer = answers.filter_by(correct = 1).first()
        answers = answers.all()

        quiz_questions.append({
            'q': q.question_text,
            'options': [a.answer_text for a in answers],
            'correctIndex': answers.index(correct_answer),
            'correctResponse': 'Good job !',
            'incorrectResponse': 'That\'s the wrong answer.'
        })

    return quiz_questions