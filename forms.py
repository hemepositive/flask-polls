from flask.ext.wtf import Form, TextField, PasswordField, IntegerField, SelectField #, BooleanField
from flask.ext.wtf import Required, EqualTo, Length

class LoginForm(Form):
    name = TextField('Username', validators = [Required(),
        Length(min=6, max=16)])
    password = PasswordField('Password', validators = [Required(),
        Length(min=6, max=16)])


class PollForm(Form):
    """ For creating a Poll from /admin """
    question = TextField('Question', validators = [Required(),
        Length(max=80)])


class ChoiceForm(Form):
    """ For creating a Poll from /admin """
    choice =TextField('Question', validators = [Required(),
        Length(max=80)])


''' To create more than two choices:
-Use seperate forms for Poll(question) and Choices(answers)
-Join the Choices to the Poll db object


class PollForm(Form):
    """ For creating a Poll from /admin """
    question = TextField('Question', validators = [Required(),
        Length(max=80)])
    first_choice =TextField('Question', validators = [Required(),
        Length(max=80)])
    second_choice =TextField('Question', validators = [Required(),
        Length(max=80)])
'''
