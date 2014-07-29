Part of the problem of being a self-taught programmer lies in the myriad ways that a technique is presented in tutorials and documentation. The most obvious case of this I have found is in the documentation for SQLALchemy and Flask-SQLAlchemy. Looking over all the different tutorials and examples I found many different ways to establish relationships, using declarative base and not using it, using __init__ and not using it, etc. I hope the follwoing is useful for someone.

Flask-SQLAlchemy is different than are "regular" SQLAlchemy:

Queries from Flask-SQLAlchemy documentation use the following syntax:
users = User.query.all()
The same query with SQLAlchemy:
db.session.query(User).all()

An important difference is the Flask-SQLAlchemy object creates a query object on each of your models thus adding useful methods such as get_or_404() which is not available in "plain" SQLAlchemy. Indeed if you try the following
db.session.query(User).get_or_404(1) you get an AttributError stating that the query object has no attribute "get_or_404"

Combining the two techniques can be useful:
For example Flask-SQLAlchemy does not have an equvalent to the SQLAchemy update method so I used the db.session syntax to do update a record after using the .

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

The backref is useful.

__init__ in models not necessary. Things like pub_date using datetime can be created in view.

It is possible to place the ForeignKey column and relationship column in one class rather than splitting them up (one-many).

If you are creating a class object (model)  that will have a relationship to another model, all of the objects need to be created and "assigned" before commiting to database as the unique ids are required for assignment/relationship.
