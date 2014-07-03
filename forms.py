from flask.ext.wtf import Form, TextField, PasswordField, IntegerField, SelectField #, BooleanField
from flask.ext.wtf import Required, EqualTo, Length

class LoginForm(Form):
	name = TextField('Username', validators = [Required(), Length(min=6, max=16)])
	password = PasswordField('Password', validators = [Required(), Length(min=6, max=16)])

class PollForm(Form):
	answer = SelectField('Choose one', validators = [Required()], choices =[('Yes', 'yes'), ('No', 'no')])