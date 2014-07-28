from flask.ext.wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import Required, Length


class LoginForm(Form):
    name = TextField('Username', validators = [Required(),
        Length(min=6, max=16)])
    password = PasswordField('Password', validators = [Required(),
        Length(min=6, max=16)])

#A single Form for question and answers does not allow for >2 questions
#Could use seperate Choice form as below but more difficult to create new poll

class NewPollForm(Form):
    """ For creating a Poll from /admin """
    question = TextField('Question', validators = [Required(),
        Length(max=80)])
    first_choice =TextField('Question', validators = [Required(),
        Length(max=80)])
    second_choice =TextField('Question', validators = [Required(),
        Length(max=80)])


class PollForm(Form):
    """ For editing a Poll from /admin """
    question = TextField('Question', validators = [Required(),
        Length(max=80)])


class ChoiceForm(Form):
    """ For editing a Poll from /admin """
    choice =TextField('Question', validators = [Required(),
        Length(max=80)])


