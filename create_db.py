from views import db
from models import Poll, Choice
from datetime import date

db.create_all()

#y = Choice('yes')
#n = Choice('no')
p = Poll('Will you go with me?')
p.question = Choice('yes')
p.question = Choice('no')
db.session.add(p)
db.session.commit()

polls = db.session.query(Poll).all()
for e in polls:
    print e

'''
from views import db
from models import FTasks
from datetime import date

# create the database and the db table
db.create_all()

# insert data
db.session.add(FTasks("Finish this tutorial", date(2014, 3, 13),
10, 1))
db.session.add(FTasks("Finish Real Python", date(2014, 3, 13), 10,
1))

# commit the changes
db.session.commit()

from views import db
from datetime import datetime
from config import DATABASE_PATH
import sqlite3

with sqlite3.connect(DATABASE_PATH) as connection:

# get a cursor object used to execute SQL commands
c = connection.cursor()

# temporarily change the name of ftasks table
c.execute("""ALTER TABLE ftasks RENAME TO old_ftasks""")

# recreate a new ftasks table with updated schema
db.create_all()

# retrieve data from old_ftasks table
c.execute("""SELECT name, due_date, priority,
status FROM old_ftasks ORDER BY task_id ASC""")

# save all rows as a list of tuples; set posted_date to now and
user_id to 1
data = [(row[0], row[1], row[2], row[3],
datetime.now(), 1) for row in c.fetchall()]

# insert data to ftasks table
c.executemany("""INSERT INTO ftasks (name, due_date, priority,
status,
posted_date, user_id) VALUES (?, ?, ?, ?, ?,
?)""", data)

# delete old_ftasks table
c.execute("DROP TABLE old_ftasks")
'''
