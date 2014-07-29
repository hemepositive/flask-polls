from app import app, db
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from functools import wraps
from forms import LoginForm, PollForm, ChoiceForm, NewPollForm
from models import Poll, Choice

# our login required decorator for the admin url
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash("You need to login correctly.")
            return redirect(url_for('login'))
    return wrap

# like django => no login on home page; just admin
@app.route('/')
def index():
    error = None
    polls = db.session.query(Poll).all()
    return render_template('index.html',
                            polls=polls,
                            error = error)

'''
@app.route('/admin', methods=['GET','POST'])
def login():
    error = None
    form = LoginForm()
    if form.validate_on_submit():
        if form['username'] != app.config['USERNAME'] or \
                form['password'] != app.config['PASSWORD']:
            error = 'Error with admin username or password. Try again'
            #flash('Error with admin username or password. Try again')
        else:
            session['logged_in'] = True
            return redirect(url_for('edit'))
    return render_template("login.html",
                           form=form,
                           error=error)
'''

@app.route('/admin', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm()
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or\
                request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            return redirect(url_for('edit'))
    return render_template('login.html', error=error, form=form)


@app.route('/edit', methods=['GET','POST'])
#@login_required
def console():
    return "You are in edit"

@app.route('/detail/<int:poll_id>', methods=['GET','POST'])
def detail(poll_id):
    # reassigning poll_id  to current_poll (why?)
    current_poll = poll_id
    poll = Poll.query.get_or_404(current_poll)
    return render_template('detail.html', poll=poll)

@app.route('/vote/<int:choice_id>', methods=['GET','POST'])
def vote(choice_id):
    # reassigning poll_id  to current_poll (why?)
    current_id = choice_id
    # using fisrt_or_404 but does not work using db.session
    choice = Choice.query.filter_by(id=current_id).first_or_404()
    print choice.votes
    new_total = choice.votes + 1
    print choice.votes
    # db.session for updating
    db.session.query(Choice).filter_by(id=current_id).update({
        "votes": new_total})
    db.session.commit()
    flash('Thanks for your vote!')
    # could send to results of this poll only but would use poll_id
    return redirect(url_for('results'))

@app.route('/results')
def results():
    polls = db.session.query(Poll).all()
    return render_template('results.html', polls=polls)

'''
ANOTHER EXAMPLE: id NOT reassigned
@app.route('/todos/<int:id>')
def todo_read(id):
    todo = Todo.query.get_or_404(id)
    return _todo_response(todo)
'''

@app.route('/create', methods = ['GET','POST'])
#@login_required
def create_poll():
    """ Function that allows admin to create a new poll """
    error = None
    poll_form = NewPollForm(crsf_enabled=False)
    if poll_form.validate_on_submit():
        new_poll = models.Poll(request.form['question'])
        first_choice = models.Choice(request.form['first_choice'])
        first_choice = models.Choice(request.form['second_choice'])
        # add choices to new_poll
        new_poll.choices = first_choice
        new_poll.choices = second_choice
        # now the database stuff
        db.session.add(new_poll)
        db.commit()
        flash("New poll created.")
        return redirect(url_for('admin'))
    else:
        error = "Error in creation. Retry"
        redirect(url_for('create_poll', error=error))
    return render_template('create.html', form=poll_form, error=error)

'''
from: http://www.pythoncentral.io/overview-sqlalchemys-expression-language-orm-queries/
>>> john = Employee(name='john')
>>> it_department = Department(name='IT')
>>> john.department = it_department
>>> s = session()
>>> s.add(john)
>>> s.add(it_department)
>>> s.commit()
>>> it = s.query(Department).filter(Department.name == 'IT').one()
>>> it.employees
[]
>>> it.employees[0].name
u'john'
'''

@app.route('/update/<int:post_id>', methods=['GET','POST'])
def update(post_id):
    """Update a poll from database"""
    try:
        poll_form = PollForm(crsf_enabled=False)
        choice_form = ChoiceForm(crsf_enabled=False)
        current_poll = poll_id
        poll = db.session.query(Poll).get(poll_id=current_poll)

        db.session.query(models.Flaskr).filter_by(post_id=new_id).delete()
        db.session.commit()
        flash('The poll has been updated.')
    except Exception as e:
        result = { 'status':0, 'message': repr(e) }
    return jsonify(result)

@app.route('/delete/<int:poll_id>', methods=['GET','POST'])
def delete(poll_id):
    """Deletes a poll from database"""
    try:
        current_poll = poll_id
        db.session.query(Poll).filter_by(poll_id=current_poll).delete()
        db.session.commit()
        flash('The poll was deleted.')
    except Exception as e:
        flash("Error. Sending back to admin page.")
        redirect(url_for('admin'))
    return redirect(url_for('admin'))

@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    flash('Admin logged out.')
    return redirect (url_for('index'))

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,error), 'error')

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@app.errorhandler(401)
def internal_error(error):
    return render_template('401.html'), 401

@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404

