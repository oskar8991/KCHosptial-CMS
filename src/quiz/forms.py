from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, ValidationError
from wtforms.validators import DataRequired, Required
from models import Questions, Content

class QuestionForm(FlaskForm):
    question = StringField('Question', validators=[DataRequired()])
    first_answer = StringField('First Answer', validators=[DataRequired()])
    second_answer = StringField('Second Answer', validators=[DataRequired()])
    third_answer = StringField('Third Answer', validators=[DataRequired()])
    correct_answer = StringField('Correct Answer', validators=[DataRequired()])
    content = SelectField('Section', validators = [Required()], coerce=int)
    submit = SubmitField('Submit')
    new_question = True # Make this false if the form is used to edit a question.

    def validate_question(self, question):
        if self.new_question and Questions.query.filter_by(question_text=question.data).first():
            raise ValidationError('This question already exists. Please make a different one.')