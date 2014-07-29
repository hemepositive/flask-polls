# My Experience With Flask-SQLAlchemy

Part of the problem of being a self-taught programmer lies in the myriad ways that a technique is presented in tutorials and documentation. The most obvious case of this I have found is in the documentation for SQLALchemy and Flask-SQLAlchemy. Looking over all the different tutorials and examples I found many different ways to establish relationships, using declarative base and not using it, using __init__ and not using it, etc. I hope the follwoing is useful for someone.


*Reading the official SQLAlchemy documentation is overwhelming.
 It is long, dense, and references things like declarative base, mappings, etc that you do not need if using Flask-SQLAlchemy.
 Focus on the Flask-SQLAlchemy documentation and examples of the same.

*Flask-SQLAlchemy is different than are "regular" SQLAlchemy:

*Queries are different for the two versions:
 Flask-SQLAlchemy Query syntax:
 `users = User.query.all()`
 SQLAlchemy syntax:
 `db.session.query(User).all()`

*The query methods use different methods.
 An important difference is the Flask-SQLAlchemy object creates a query object on each of your models thus adding useful methods such as get_or_404() which is not available in "plain" SQLAlchemy. Indeed if you try the following
 `db.session.query(User).get_or_404(id)` you get an AttributError stating that the query object has no attribute "get_or_404"

*One can mix and match the two to meet specific needs:
 For example Flask-SQLAlchemy does not have an equivalent to the SQLAchemy update method.
 1. Use Flask-SQLAlchemy's first_or_404() method to query the db in a web-centric way.
 `u = User.query.filter_by(id=user_id).first_or_404()`
 2. Use SQLAlchemy's update methodfollowed by db.session.(Model).update() method.
 `db.session.(User).update({'name':'Gord'})`

*The backref *name* is the singular of the __tablename__.

*__init__ method in models not necessary.
 The model object and attributes can be instanced in the view

*There are options in where relationship/ForiegnKey columns go in the models.
 1. Typically ForeignKey column is placed in the "many" Model and relationship column is placed in the "one" Model.
 [here](https://pythonhosted.org/Flask-SQLAlchemy/models.html)
 ```
 class Person(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(50))
     addresses = db.relationship('Address', backref='person',
                                lazy='dynamic')

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
 ```
 2. Alternatively both columns can be placed in the "many".
 [here](http://lucumr.pocoo.org/2011/7/19/sqlachemy-and-you/)
 ```
 from sqlalchemy import Column, Integer, String, ForeignKey
 from sqlalchemy.orm import relationship, backref

 class Manufacturer(Base):
     __tablename__ = 'manufacturers'
     id = Column(Integer, primary_key=True)
     name = Column(String(30))

 class Car(models.Model):
     __tablename__ = 'cars'
     id = Column(Integer, primary_key=True)
     manufacturer_id = Column(Integer, ForeignKey('manufacturers.id'))
     name = Column(String(30))

     manufacturer = relationship('Manufacturer', backref=
        backref('cars', lazy='dynamic'))
 ```
??????
*Order of Model instantiation matters.
 You cannot form a relationship with a Model/object that does not exist. The "one" Model requires the "many" Models' unique id if the many model uses an
 __init__??
 ? One could create and add the relationship later I suppose. Like adding another choice to a Poll

*Examples for SQLAlchemy:
[here](http://lucumr.pocoo.org/2011/7/19/sqlachemy-and-you/)
DELETE
obj = MyModel.query.get(the_id)
session.delete(obj)

UPDATE
obj = MyModel.query.get(the_id)
obj.name = 'New Value'
session.commit()
