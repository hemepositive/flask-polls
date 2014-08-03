from app import app, db
from flask import flash, redirect, render_template, request, session, url_for
from functools import wraps
from forms import LoginForm, PollForm, ChoiceForm, NewPollForm, ChoicesForm
from models import Poll, Choice, Admin

'''
django-polls creates a new poll question first then questions added in
a second function.

django-polls allows for unlimited questions. Current MVP version with only two.
'''

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
    form = LoginForm()
    if request.method == 'GET':
        return render_template("login.html",
                               form=form,
                               error=error
                               )
    if request.method=='POST':
        admin_user = db.session.query(Admin).filter_by(
            username=form.name.data,
            password=form.password.data
            )
        if admin_user is None:
            error = 'Invalid username or password.'
        else:
            #print admin_user
            session['logged_in'] = True
            #session['user_id'] = u.id
            #session['user_id'] = admin_user.id
            flash('You are logged in. Go Crazy.')
            return redirect(url_for('admin_main'))

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
    # using fisrt_or_404 from Flakl_SQLAlchemy
    choice = Choice.query.filter_by(id=current_id).first_or_404()
    new_total = choice.votes + 1
    # db.session for updating
    db.session.query(Choice).filter_by(id=current_id).update({
        "votes": new_total})
    db.session.commit()
    flash('Thanks for your vote!')
    # could send to results of this poll only but would need poll_id
    return redirect(url_for('results'))

@app.route('/results')
def results():
    polls = db.session.query(Poll).all()
    return render_template('results.html', polls=polls)


@app.route('/admin_main', methods=['GET','POST'])
@login_required
def admin_main():
    """ Skipping django main with CRUD for all models.
    Going instead to url with 'add_poll' and 'change_poll'.
    """
    form = PollForm(csrf_enabled=False)
    polls = Poll.query.all()
    return render_template('admin_main.html',
                           form=form,
                           polls=polls)

@app.route('/add_poll', methods = ['GET','POST'])
@login_required
def add_poll():
    """ Function that allows admin to create a new poll """
    error = None
    form = PollForm(csrf_enabled=False)
    if form.validate_on_submit():
        new_poll = Poll(form.question.data)
        db.session.add(new_poll)
        db.session.commit()
        flash('New entry was successfully posted. Thanks.')
    else:
        flash_errors(form)
    return redirect(url_for('admin_main'))

'''
# ORIGINAL

@app.route('/update/<int:poll_id>', methods=['GET','POST'])
def update(poll_id):
    """Update a poll from database"""
    error = None
    poll = Poll.query.get_or_404(poll_id)
    form = ChoicesForm(csrf_enabled=False)
    if form.validate_on_submit():
        current_poll = poll_id
        poll = Poll.query.get_or_404(current_poll)
        first_choice = models.Choice(form.choice_one.data)
        second_choice = models.Choice(form.choice_two.data)
        # add choices to new_poll
        db.session.poll.choices = first_choice
        db.session.poll.choices = second_choice
        # now the database stuff
        db.session.add_all([first_choice, second_choice])
        db.session.commit()
        flash("New choices created.")
        return redirect(url_for('admin_main'))

    else:
        error = "Error in creation. Retry"
        redirect(url_for('update', error=error))
    """
    or

    else:
        flash_errors(form)
    """
    #return "You are at update!"
    return render_template('update.html',
                           form=form,
                           error=error,
                           poll=poll)
'''

@app.route('/update/<int:poll_id>', methods=['GET','POST'])
def update(poll_id):
    """Update a poll from database"""
    if request.method == 'GET':
        error = None
        poll = Poll.query.get_or_404(poll_id)
        form = ChoicesForm(csrf_enabled=False)
        return render_template('update.html',
                           form=form,
                           error=error,
                           poll=poll)
    if request.method == 'POST':
        current_poll = poll_id
        poll = Poll.query.get_or_404(current_poll)
        first_choice = models.Choice(form.choice_one.data)
        second_choice = models.Choice(form.choice_two.data)
        # add choices to new_poll
        db.session.poll.choices = first_choice
        db.session.poll.choices = second_choice
        # now the database stuff
        db.session.add_all([first_choice, second_choice])
        db.session.commit()
        flash("New choices created.")
        return redirect(url_for('admin_main'))

    else:
        error = "Error in creation. Retry"
        #redirect(url_for('update', error=error)
        return "You are at update!"



@app.route('/delete/<int:poll_id>', methods=['GET','POST'])
def delete(poll_id):
    """Deletes a poll from database
    Does not delete choices yet.
    """
    try:
        current_id = poll_id
        print current_id
        #obj = MyModel.query.get(the_id)
        #session.delete(obj)
        #db.session.query(Poll).delete(current_poll)
        poll_for_delete = Poll.query.get_or_404(current_id)
        db.session.delete(poll_for_delete)
        db.session.commit()
        flash('The poll was deleted.')
    except Exception as e:
        flash("Error. Sending back to admin page.")
        redirect(url_for('admin_main'))
    return redirect(url_for('admin_main'))

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


'''
ANOTHER EXAMPLE: id NOT reassigned
@app.route('/todos/<int:id>')
def todo_read(id):
    todo = Todo.query.get_or_404(id)
    return _todo_response(todo)


# work in progress
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
