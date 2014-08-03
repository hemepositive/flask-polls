from flask.ext.wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Length


class LoginForm(Form):
    name = TextField('Username', validators = [DataRequired(),
        Length(min=6, max=16)])
    password = PasswordField('Password', validators = [DataRequired(),
        Length(min=6, max=16)])

#A single Form for question and answers does not allow for >2 questions
#Could use seperate Choice form as below but more difficult to create new poll

class NewPollForm(Form):
    """ For creating a Poll from /admin """
    question = TextField('Question', validators = [DataRequired(),
        Length(max=200)])
    first_choice =TextField('First choice', validators = [DataRequired(),
        Length(max=200)])
    second_choice =TextField('Second choice', validators = [DataRequired(),
        Length(max=200)])


class PollForm(Form):
    """ For editing a Poll from /admin """
    question = TextField('Question', validators = [DataRequired(),
        Length(max=200)])


class ChoiceForm(Form):
    """ For editing a Poll from /admin """
    choice =TextField('Question', validators = [DataRequired(),
        Length(max=200)])

class ChoicesForm(Form):
    """ For editing a Poll from /admin """
    choice_one =TextField('First question', validators = [DataRequired(),
        Length(max=200)])
    choice_two =TextField('Second question', validators = [DataRequired(),
        Length(max=200)])


