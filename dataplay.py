from app import db
from app.models import Poll, Choice, Admin
from datetime import date

#db.drop_all()
#db.create_all()

polls = db.session.query(Poll).all()
print type(polls)
for e in polls:
    print e.id
    print e.question
    print e.pub_date
    print e.choices

choices = db.session.query(Choice).all()
for e in choices:
    print e.id
    print e.poll

print "\n================"
print "===== Admin ===="
print "================"
admins = db.session.query(Admin).all()
for admin in admins:
    print admin.id
    print admin.username
    print admin.password


'''
>>> polls = Poll.query.all()
>>> polls
[<Poll u'Will you go with me?'>, <Poll u'Can I call you sometime?'>, <Poll u'You got a phone number?'>]
>>> for p in polls:
...     print p.choices
...
[<Choice u'yes'>, <Choice u'no'>]
[<Choice u'sure'>, <Choice u'nope'>]
[<Choice u'NO!'>, <Choice u'Phone company turned it off.'>]
>>> p = Poll.query.get(3)
>>> p.question
u'You got a phone number?'
>>> p.choices
[<Choice u'NO!'>, <Choice u'Phone company turned it off.'>]
>>> p.choices[0].id
5
>>> p.choices[1].id
6
>>> p.id
3

ANOTHER: you have to update the specific choice using choice.id

>>> db.session.query(Choice).filter_by(poll_id=3).update({'choice_text':'YESS!'})
2
>>> db.session.commit()
>>> choices = Choice.query.all()
>>> choices
[<Choice u'yes'>, <Choice u'no'>, <Choice u'sure'>, <Choice u'nope'>, <Choice u'YESS!'>, <Choice u'YESS!'>]
>>>

BETTER WAY:
>>> db.session.query(Choice).filter_by(poll_id=3).update({'choice_text':'YESS!'})
2
>>> db.session.commit()
>>> choices = Choice.query.all()
>>> choices
[<Choice u'yes'>, <Choice u'no'>, <Choice u'sure'>, <Choice u'nope'>, <Choice u'YESS!'>, <Choice u'YESS!'>]
>>> db.session.query(Choice).filter_by(id=6).update({'choice_text':'NEVER!'})
1
>>> db.session.commit()
>>> choices = Choice.query.all()
>>> choices
[<Choice u'yes'>, <Choice u'no'>, <Choice u'sure'>, <Choice u'nope'>, <Choice u'YESS!'>, <Choice u'NEVER!'>]
>>>
'''
