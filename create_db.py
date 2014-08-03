from app import db
from app.models import Poll, Choice, Admin
from datetime import date

db.drop_all()
db.create_all()

# playing around with multiple ways to create db obects

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
#db.session.commit()

q = Poll('You got a phone number?')
a = Choice('NO!')
b = Choice('YESS!.')
a.poll = q
b.poll = q
db.session.add_all([a, b, q])

admin = Admin(username='admin', password='admin')
db.session.add(admin)

db.session.commit()

