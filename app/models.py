from app import db
from datetime import date


class Poll(db.Model):

    __tablename__ = "polls"

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    pub_date = db.Column(db.Date)
    choices = db.relationship("Choice", backref="poll")

    def __init__(self, question, pub_date=None):
        self.question = question
        if pub_date == None:
            today = date.today()
        self.pub_date = today

    def __repr__(self):
        return "<Poll %r>" % self.question

    # could create a decorator for was_published_recently

class Choice(db.Model):

    __tablename__ = "choices"

    id = db.Column(db.Integer, primary_key=True)
    choice_text = db.Column(db.String(200))
    votes = db.Column(db.Integer)
    # db.ForeignKey("use___tablename__.id")
    poll_id = db.Column(db.Integer, db.ForeignKey("polls.id"))

    def __init__(self, choice_text, poll_id=None, votes=0):
        # initing the poll_id which may be a problem
        # setting to None on init in case Poll created before Choice
        # use backref to assign poll_id
        self.choice_text = choice_text
        self.poll_id = poll_id
        self.votes = votes

    def __repr__(self):
        return "<Choice %r>" % self.choice_text


class Admin(db.Model):

    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    # passing on making relationships with Poll(s) for now
    # passing on __init__ as optional

    def __repr__(self):
        return "<Admin %r>" % self.username





"""
Models from DJANGO POLLS:

**Initial version**
class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

**Final version**
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
