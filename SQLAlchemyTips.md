# My Experience With Flask-SQLAlchemy

Part of the problem of being a self-taught programmer lies in the myriad ways that a technique is presented in tutorials and documentation. The most obvious case of this I have found is in the documentation for SQLALchemy and Flask-SQLAlchemy. Looking over all the different tutorials and examples I found many different ways to establish relationships, using declarative base and not using it, using \_\_init\_\_ and not using it, etc. I hope the following is useful for someone.


*Reading the official SQLAlchemy documentation is overwhelming.
It is long, dense, and references things like declarative base, mappings, etc that you do not need if using Flask-SQLAlchemy.
 Focus on the Flask-SQLAlchemy documentation and examples of the same.

*Flask-SQLAlchemy is different than are "regular" SQLAlchemy:

*Queries are different for the two versions:

  1. Flask-SQLAlchemy Query syntax:
  `users = User.query.all()`

  2. SQLAlchemy syntax:
 `db.session.query(User).all()`

*The query methods use different methods.
An important difference is the Flask-SQLAlchemy object creates a query object on each of your models thus adding useful methods such as get_or_404() which is not available in "plain" SQLAlchemy. Indeed if you try the following
 `db.session.query(User).get_or_404(id)` you get an AttributError stating that the query object has no attribute "get\_or\_404"

*One can mix and match the two to meet specific needs.
For example Flask-SQLAlchemy does not have an equivalent to the SQLAchemy update method.

 1. Use Flask-SQLAlchemy's first_or_404() method to query the db in a web-centric way.

 `u = User.query.filter_by(id=user_id).first_or_404()`

 2. Use SQLAlchemy's update methodfollowed by db.session.(Model).update() method.

 `db.session.(User).update({'name':'Gordon'})`

*The "name" variable in backref="name" is the singular of the \_\_tablename\_\_.

*\_\_init\_\_ method in models not necessary.
 The model object and attributes can be instanced in the view.

*There are options in where relationship/ForiegnKey columns go in the models.

 1. Typically ForeignKey column is placed in the "many" Model and relationship column is placed in the "one" Model.
CANNOT GET MARKDOWN FORMATTING TO WORK FOR ME!
 [link](https://pythonhosted.org/Flask-SQLAlchemy/models.html)


```python
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    addresses = db.relationship('Address', backref='person',
                                                 lazy='dynamic')
```

```python
   class Address(db.Model):
         id = db.Column(db.Integer, primary_key=True)
         email = db.Column(db.String(50))
         person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
```
 2. Alternatively both columns can be placed in the "many".
 [link](http://lucumr.pocoo.org/2011/7/19/sqlachemy-and-you/)

```python
 from sqlalchemy import Column, Integer, String, ForeignKey
 from sqlalchemy.orm import relationship, backref
```
```python
 class Manufacturer(Base):
     \_\_tablename\_\_ = 'manufacturers'
     id = Column(Integer, primary_key=True)
     name = Column(String(30))
```
```python
 class Car(models.Model):
     \_\_tablename\_\_ = 'cars'
     id = Column(Integer, primary_key=True)
     manufacturer_id = Column(Integer, ForeignKey('manufacturers.id'))
     name = Column(String(30))
```
     `manufacturer = relationship('Manufacturer', backref=
        backref('cars', lazy='dynamic'))`

*Order of Model instantiation matters.

 Still working this one out.


*Examples for SQLAlchemy:
[link](http://lucumr.pocoo.org/2011/7/19/sqlachemy-and-you/)

DELETE


`obj = MyModel.query.get(the_id)`

`session.delete(obj)`


UPDATE


`obj = MyModel.query.get(the_id)`

`obj.name = 'New Value'`

`session.commit()`
