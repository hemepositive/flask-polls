from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)

class Admin(db.Model):

    __tablename__ = "admin"

    admin_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(16), nullable=False)
    #not sure that at most basic level the Poll class needs link to Admin class
    #poll = db.relationship('Poll', backref = "administrator")
    
    def __init__(self, name, password):
        self.name = name
        self.password = password

    def __repr__(self):
        return '<Admin %r>' % self.name


class Poll(db.Model):

    __tablename__ = "poll"

    pid = db.Column(db.Integer, primary_key=True) #not using .id
    question = db.Column(db.String(80), nullable=False)
    pub_date = db.Column(db.DateTime)
    choices = db.relationship('Choice', backref='the_poll')

    def __init__(self, question=None, pub_date=None):
        self.question = question
        # unsure if the following is required if using SQLAlchemy Date Type
        if pub_date is None:
            pub_date = date.today()
        self.pub_date = pub_date
        
    def __repr__(self):
        return "<Poll %r>" % self.question

class Choice(db.Model):

	__tablename__ = "choice"

	id = db.Column(db.Integer, primary_key=True)
	choice_text = db.Column(db.String(200))
	votes = db.Column(db.Integer)
	the_poll_id = db.Column(db.Integer, db.ForeignKey('poll.pid'))

	def __init__(self, poll_id, choice_text=None, votes = 0):
            self.poll_id = poll_id
	    self.choice_text = choice_text
	    # starting value for votes is 0
	    self.votes = votes
		
		

	def __repr__(self):
    	    return "<Choice %r>" % self.choice_text
