# django has a settings.py file in level above the current app's main folder


import os

basedir = os.path.abspath(os.path.dirname(__file__))

# "The config is actually a subclass of a dictionary and 
#        can be modified just like any dictionary: " 
#     			 --from http://flask.pocoo.org/docs/config/
#  The full list of config options are linked above
#  So to be different I will set debug to True here and simplify our run.py

DATABASE = "pollr.db"
SECRET_KEY = "my_secret_key_of_hiding"
DEBUG = True

DATABASE_PATH = os.path.join(basedir, DATABASE)

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH