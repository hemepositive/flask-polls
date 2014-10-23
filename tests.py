import os
import unittest
from app import app, db
from config import basedir
from app.models import Poll, Choice, Admin

TEST_DB = 'test.db'

class AllTests(unittest.TestCase):
    # the setup
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_TESTING'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()
        
    def tearDown(self):
        db.drop_all()
        
    def test_admin_user_creation(self):
        admin_user = Admin(
            username='test_username', 
            password= 'test_password'
        )
        db.session.add(admin_user)
        db.session.commit()
        
        
    
if __name__ == "__main__":
    unittest.main()