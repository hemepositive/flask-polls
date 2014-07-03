from app import app, db
from flask import Flask, flash, redirect, render_template.
    request, session, url_for #,g
from functools import wraps
from app.forms import PollForm, LoginForm
from app.models import Admin, Poll, Choice

def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash("You need to login correctly.")
		    return redirect(url_for,'login')
	return wrap

@app.route('/', methods=['GET', 'POST'])
def mainPage():
	if request.method == 'POST':
		#out = str(request.form['answer'])
		flash("Thank you for your answer!")
		return render_template('bye.html')
	else:
		render_template('poll.html', form = PollForm(request.form), error=error)

app.route('/admin', methods=['GET', 'POST'])
def login():
	error = None
	if request.method =='POST':
		u = User.query.filter_by(name=request.form['name'], password=request.form['password']).first()
		if u is None:
			error = "You are not the master of this poll."
		else:
			session['logged_in'] = True
			session['user_id'= u.id
			flash('Manipulate the polls as you will, Master.')
			return redirect(url_for('master'))

app.route('/votes')
def get_votes():
	pass
	'''
	question = db.session.query(Poll).filter_by() #???
	yeas = db.session.query(Choice).filter_by()
	nays = db.session.query(Choice).filter_by()
    '''
app.route('/make_poll', methods = ['GET','POST'])
@login_required()
""" Here lies CRUD actions for the admin """
def make_poll():
	#flash("Here is where admin can manage 'polls'. ")
	page = """ <html>
	       <a href="{url_for('mainPage')}">click here to go to main </a>
	       </html>"""