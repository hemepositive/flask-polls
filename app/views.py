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

@app.route('/admin', methods=['GET', 'POST'])
def login():
    error = None
    if request.method=='POST':
        if request.form['username'] != app.config['USERNAME'] or \
            request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You are logged in. Poll it up!.')
            return redirect(url_for('editor'))
    return render_template("login.html",
                           form = LoginForm(),
                           error = error)

@app.route('/detail/<int:poll_id>', methods=['GET', 'POST'])
def detail(poll_id):
    # reassigning poll_id  to current_poll for some reason
    current_poll = poll_id
    poll = db.session.query(Poll).get(current_poll)
    return render_template('detail.html', poll=poll)

@app.route('/vote/<int:choice_id>', methods=['POST'])
def vote(poll_id):
    # reassigning poll_id  to current_poll for some reason
    current_choice = choice_id
    choice = db.session.query(Choice).get(choice_id=current_choice)
    new_total = choice.votes + 1
    db.session.query(Choice).filter_by(choice_id=current_choice).update({
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
@app.route('/complete/<int:task_id>/',)
@login_required
def complete(task_id):
new_id = task_id
db.session.query(FTasks).filter_by(task_id=new_id).update({"status":"0"})
db.session.commit()
flash('The task was marked as complete. Nice.')
return redirect(url_for('tasks'))

ANOTHER EXAMPLE: id NOT reassigned
@app.route('/todos/<int:id>')
def todo_read(id):
    todo = Todo.query.get_or_404(id)
    return _todo_response(todo)
'''

@app.route('/create', methods = ['GET','POST'])
@login_required
def create_poll():
    """ Function that allows admin to create a new poll """
    error = None
    poll_form = NewPollForm()
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
    return render_template('create.html', form=form, error=error)


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

'''
@app.route('/create', methods = ['GET','POST'])
@login_required()
def create_poll():
    """ Function that allows admin to create a new poll """
    poll_form = PollForm()
    first_choice_form = ChoiceForm()
    second_choice_form = ChoiceForm()
    if poll_form.validate_on_submit() and \
        first_choice_form.validate_on_submit() and \
        second_choice_form.validate_on_submit():
        new_poll = models.Poll(request.form['question'])
        new_poll.session.add(choices = request.form['first_choice'])
        new_poll.session.add(choices = request.form['second_choice'])
    pass


@app.route('/create', methods=['GET','POST'])
@login_required
def create_poll():
    """Creates a new poll in the database"""
    if not session.get('logged_in'):
        abort(401)
    poll_form = PollForm()
    choice_form = ChoiceForm()
    if form_validate_on_submit():
        new_poll = models.Poll(request.form['question'],
                           request.form['first_choice'],
                           request.form['second_choice'])
    db.session.add(new_poll)
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('admin'))
'''

@app.route('/update/<int:post_id>', methods=['GET','POST'])
def update(post_id):
    """Update a poll from database"""
    try:
        poll_form = PollForm()
        choice_form = ChoiceForm()
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


if __name__ == '__main__':
    app.run()


"""
# views.py


from app import app, db
from flask import Flask, flash, redirect, render_template, request, session, url_for, g
from functools import wraps
from app.forms import AddTask, RegisterForm, LoginForm
from app.models import FTasks, User
from sqlalchemy.exc import IntegrityError

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    flash('You are logged out. Bye. :(')
    return redirect (url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method=='POST':
        u = User.query.filter_by(name=request.form['name'],
                          password=request.form['password']).first()
        if u is None:
            error = 'Invalid username or password.'
        else:
            session['logged_in'] = True
            session['user_id'] = u.id
            flash('You are logged in. Go Crazy.')
            return redirect(url_for('tasks'))

    return render_template("login.html",
                           form = LoginForm(request.form),
                            error = error)

@app.route('/tasks/')
@login_required
def tasks():
    open_tasks = db.session.query(FTasks).filter_by(status='1').order_by(
                    FTasks.due_date.asc())
    closed_tasks = db.session.query(FTasks).filter_by(status='0').order_by(
                    FTasks.due_date.asc())
    return render_template('tasks.html',form = AddTask(request.form),
                            open_tasks=open_tasks, closed_tasks=closed_tasks)

# Add new tasks:
@app.route('/add/', methods=['GET', 'POST'])
@login_required
def new_task():
    form = AddTask(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        new_task = FTasks(
                    form.name.data,
                    form.due_date.data,
                    form.priority.data,
                    form.posted_date.data,
                    '1',
                    session['user_id']
                    )
        db.session.add(new_task)
        db.session.commit()
        flash('New entry was successfully posted. Thanks.')
    else:
        flash_errors(form)
    return redirect(url_for('tasks'))

# Mark tasks as complete:
@app.route('/complete/<int:task_id>/',)
@login_required
def complete(task_id):
    new_id = task_id
    db.session.query(FTasks).filter_by(task_id=new_id).update({"status":"0"})
    db.session.commit()
    flash('The task was marked as complete. Nice.')
    return redirect(url_for('tasks'))

# Delete Tasks:
@app.route('/delete/<int:task_id>/',)
@login_required
def delete_entry(task_id):
    new_id = task_id
    db.session.query(FTasks).filter_by(task_id=new_id).delete()
    db.session.commit()
    flash('The task was deleted. Why not add a new one?')
    return redirect(url_for('tasks'))

@app.route('/register/', methods=['GET','POST'])
def register():
    error = None
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
     new_user = User(
                 form.name.data,
                 form.email.data,
                 form.password.data,
                 )
     try:
         db.session.add(new_user)
         db.session.commit()
         flash('Thanks for registering. Please login.')
         return redirect(url_for('login'))
     except IntegrityError:
         error = 'Oh no! That username and/or email already exist. Please try again.'
    else:
     flash_errors(form)
    return render_template('register.html', form=form, error=error)

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,error), 'error')

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404
"""
