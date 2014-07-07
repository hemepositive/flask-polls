from app import app, db
from flask import Flask, flash, redirect, render_template.
    request, session, url_for
from functools import wraps
from forms import PollForm, ChoiceForm, LoginForm
from models import Admin, Poll, Choice

# app and db created on __init__

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash("You need to login correctly.")
            return redirect(url_for,'login')
    return wrap

# like django => no login on home page; just admin
@app.route('/')
def index():
    error = None
    all_polls = db.session.query(Polls).all()
    return render_template('index.html', all_polls)

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
            flash('You are logged in. Poll it up!.')
            return redirect(url_for('admin'))

    return render_template("login.html",
                           form = LoginForm(request.form),
                            error = error)

app.route('/admin', methods=['GET', 'POST'])
def admin():
    error = None
    if request.method =='POST':
        u = User.query.filter_by(name=request.form['name'],
            password=request.form['password']).first()
        if u is None:
            error = "You are not the master of this poll."
        else:
            session['logged_in'] = True
            session['user_id'= u.id
            flash('Manipulate the polls as you will, Master.')
            return redirect(url_for('master'))

app.route('/votes/<int:poll_id>')
def get_votes():
    pass
    '''
    class Choice(models.Model):
    question = models.ForeignKey(Poll)
    answer = models.CharField(max_length=30)
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.answer
    ######################################################
    question = db.session.query(Poll).filter_by() #???
    yeas = db.session.query(Choice).filter_by()
    nays = db.session.query(Choice).filter_by()
    '''

app.route('/create_poll', methods = ['GET','POST'])
@login_required()
def create_poll():
    """ Function that allows admin to create a new poll """
    #flash("Here is where admin can manage 'polls'. ")
    pass

@app.route('/create', methods=['POST'])
def add_choice():
    """Adds new post to the database."""
    if not session.get('logged_in'):
        abort(401)
    new_entry = models.Flaskr(request.form['title'], request.form['text'])
    db.session.add(new_entry)
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET','POST'])
def update(post_id):
    """Update a poll from database"""
    result = { 'status':0, 'message': 'Error' }
    try:
        new_id = post_id
        db.session.query(models.Flaskr).filter_by(post_id=new_id).delete()
        db.session.commit()
        result = { 'status':1, 'message': "Post Deleted" }
        flash('The entry was deleted.')
    except Exception as e:
        result = { 'status':0, 'message': repr(e) }
    return jsonify(result)

@app.route('/delete/<int:post_id>', methods=['GET'])
def delete_entry(post_id):
    """Deletes poll from database"""
    result = { 'status':0, 'message': 'Error' }
    try:
        new_id = post_id
        db.session.query(models.Flaskr).filter_by(post_id=new_id).delete()
        db.session.commit()
        result = { 'status':1, 'message': "Post Deleted" }
        flash('The entry was deleted.')
    except Exception as e:
        result = { 'status':0, 'message': repr(e) }
    return jsonify(result)


@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    flash('You are logged out. Bye. :(')
    return redirect (url_for('login'))

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
