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
        
    def test_admin_setup(self):
        admin_user = Admin(
            username='test_username', 
            password= 'test_password'
        )
        db.session.add(admin_user)
        db.session.commit()
        
    # MODELS tests
    
    def test_admin_exists_in_database(self):
        admin_user = Admin(
            username='test_username', 
            password= 'test_password'
        )
        db.session.add(admin_user)
        db.session.commit()
        # using Flask_SQLAlchemy method
        admin_get = Admin.query.get(1)
        assert admin_get.username == 'test_username'
        assert admin_get.password == 'test_password'
        
    def test_poll_creation(self):
        new_poll = Poll(
            question='test_question?'
        )
        db.session.add(new_poll)
        db.session.commit()
        # using Flask_SQLAlchemy method
        all_polls = Poll.query.all()
        for poll in all_polls:
            poll.question
        assert poll.question == 'test_question?'
        
    def test_choice_creation(self):
        new_choice = Choice(
            choice_text = 'test this choice'
        )
        db.session.add(new_choice)
        db.session.commit()
        # using Flask_SQLAlchemy method
        all_choices = Choice.query.all()
        for choice in all_choices:
            choice.choice_text
        assert choice.choice_text == 'test this choice'
        
    def test_choice_to_poll_relationships(self):
        test_poll = Poll(
            question = "Want to do some testing?"
        )
        choice_one = Choice(
            choice_text = 'Right now!'
        )
        choice_two = Choice(
            choice_text = 'Not today.'
        )
        choice_one.poll = test_poll
        choice_two.poll = test_poll
        db.session.add_all([test_poll, choice_one, choice_two])
        db.session.commit()
        # using Flask_SQLAlchemy method
        choices = Choice.query.all()
        for entry in choices:
            entry.poll.question
        assert entry.poll.question == "Want to do some testing?"
    
    # VIEWS tests
    
    def test_url_route_for_admin(self):
        resp = self.app.get('/admin')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Flask administration', resp.data)
    
    def login_helper(self, name, password):
        ''' A helper function for testing admin '''
        return self.app.post('/admin', 
                            data=dict(
                                name=name,
                                password=password
                            ),
                            follow_redirects=True
                            )
    
    def test_true_Admin_can_access_dashboard(self):
        resp = self.login_helper('test_username', 'test_password')
        self.assertIn('Admin Console', resp.data)
        
    def test_url_route_for_admin_login_error(self):
        resp = self.login_helper('test_username', 'test_password')
        self.assertEqual(resp.status_code, 302)
    
    def test_non_Admin_cannot_access_dashboard(self):
        resp = self.login_helper('wrong', 'wrongagain')
        self.assertIn('Invalid username or password.', resp.data)
        
    
    
        
        
        
    
if __name__ == "__main__":
    unittest.main()