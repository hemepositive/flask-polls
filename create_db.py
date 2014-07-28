from app import db
from app.models import Poll, Choice
from datetime import date

db.drop_all()
db.create_all()

p = Poll('Will you go with me?')
y = Choice('yes')
y.poll = p
n = Choice('no')
n.poll = p
db.session.add_all([p,y,n])

sure = Choice('sure')
nope = Choice('nope')
new = Poll('Can I call you sometime?')
sure.poll = new
nope.poll = new
db.session.add_all([new, sure, nope])
db.session.commit()


polls = db.session.query(Poll).all()
for e in polls:
    print e

choices = db.session.query(Choice).all()
for e in choices:
    print e

