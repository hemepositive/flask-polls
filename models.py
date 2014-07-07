from app import db
from datetime import date
# < db is a SQLAlchemy object created when __init__ called >
# using the above: from app import db
# to call the SQLAlchemy Models and data Types you must use dot notation in the configuration
# in contrast to "from sqlalchemy import Model, Column, Integer, String" which would allow you
# to drop the db.Whatever

class Admin(db.Model):

    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), nullable=False)
    password = db.Column(db.String(16), nullable=False)
    #not sure that at most basic level the Poll class needs link to Admin class
    poll = db.relationship('Poll', backref = "administrator")

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def __repr__(self):
        return '<Admin %r>' % self.name


class Poll(db.Model):

    __tablename__ = "poll"

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(80), nullable=False)
    pub_date = dbi.Column(db.DateTime)
    #admin_id links to Admin with ForeignKey() passed the backref from class Admin()
    #but appears that this used more without a __tablename__
    #as noted in Flask_SQLAlchemy documentation
    #ELI5: admin_id is a database column for table poll linking Poll with Admin
    #      using dot notation with the backref property for Admin class
    #admin_id = db.Column(db.ForeignKey('admin.id'))
    choices = db.relationship('Choice', backref='poll')

    def __init__(self, question, pub_date = None):
        self.question = question
        # unsure if the following is required if using SQLAlchemy Date Type
        # just commenting out for now
        """
        if pub_date is None:
            pub_date = date.today()
        self.pub_date = pub_date
        """

    def __repr__(self):
        return "<Poll %r>" % self.question

class Choice(db.Model):

    __tablename__ = "choice"

    id = db.Column(db.Integer, primary_key=True)
    choice_text = db.Column(db.String(200))
    votes = db.Column(db.Integer)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'))

    def __init__(self, poll_id, choice_text= None, votes = None):
        self.poll_id = poll_id
        self.choice_text = choice_text
        # starting value for votes is None
        self.votes = votes

    def __repr__(self):
        return "<Choice %r>" % self.choice_text

"""
EXAMPLE OF backref() -------------------------------------------

class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    children = relationship("Child", backref="parent")

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent.id'))

END EXAMPLE-----------------------------------------------------

class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField(’date published’)

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class Poll(models.Model):
    question = models.CharField(max_length=120)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        now = timezone.now()
        return timezone.now() - datetime.timedelta(days=2) <= self.pub_date < now
    #for admin look
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = "Published recently?"

    def __unicode__(self):
        return self.question

class Choice(models.Model):
    question = models.ForeignKey(Poll)
    answer = models.CharField(max_length=30)
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.answer
"""
