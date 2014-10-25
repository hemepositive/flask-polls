# Tests for Flask-Polls Users

import os
import unittest

from app import app, db
from config import basedir
from app.models import Choice, Poll

TEST_DB = 'test.db'


class TasksTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

    # executed after to each test
    def tearDown(self):
        db.drop_all()

    ########################
    #### helper methods ####
    ########################

    def test_create_poll_for_testing(self):
        new_poll = Poll(
            question = 'This is a test question?'
        )
        db.session.add(new_poll)
        db.session.commit()
        poll_get = Poll.query.get(1)
        assert poll_get.question == 'This is a test question?'
        
    def test_create_choices_for_testing(self):
        choice_one = Choice(
            choice_text = 'Test choice one.'
        )
        choice_two = Choice(
            choice_text = 'Test choice two.'
        )
        db.session.add_all([choice_one, choice_two])
        db.session.commit()
        choices = db.session.query(Choice).all()
        choice_list = []
        for choice in choices:
            #print choice.choice_text
            choice_list.append(choice.choice_text) 
        self.assertIn('Test choice one.', choice_list)
        self.assertIn('Test choice two.', choice_list)
        
    def create_poll(self):
        new_poll = Poll(
            question = 'This is another test question?'
        )
        choice_one = Choice(
            choice_text = 'My vote is for choice one.'
        )
        choice_two = Choice(
            choice_text = 'My vote is for choice two.'
        )
        choice_one.poll = new_poll
        choice_two.poll = new_poll
        db.session.add_all([choice_one, choice_two, new_poll])
        db.session.commit()
        
    ###############
    #### views ####
    ###############

    def test_routing_to_index(self):
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Welcome to Flask-Polls', resp.data)
    

    def test_users_can_view_polls_at_index(self):
        new_poll = Poll(
            question = 'This is a test question?'
        )
        db.session.add(new_poll)
        db.session.commit()
        poll_get = Poll.query.get(1)
        assert poll_get.id == 1
        resp = self.app.get('/')
        self.assertIn('This is a test question?', resp.data)
        
        
    def test_routing_to_poll_detail(self):
        new_poll = Poll(
            question = 'This is a test question?'
        )
        db.session.add(new_poll)
        db.session.commit()
        poll_get = Poll.query.get(1)
        assert poll_get.id == 1
        resp = self.app.get('/detail/1')
        self.assertEqual(resp.status_code, 200) # Throws 404 error; WHY
        self.assertIn('Click on a choice to vote!', resp.data)
    

    def test_users_can_vote_choice_one(self):
        self.create_poll() 
        resp = self.app.get('/detail/1')
        self.assertEqual(resp.status_code, 200) 
        self.assertIn('Click on a choice to vote!', resp.data)

    '''choice = Choice.query.filter_by(id=current_id).first_or_404()
    new_total = choice.votes + 1
    # db.session for updating
    db.session.query(Choice).filter_by(id=current_id).update({
        "votes": new_total})'''
    
    def test_choices_appear_in_detail(self):
        self.create_poll() 
        resp = self.app.get('/detail/1')
        self.assertIn('My vote is for choice one.', resp.data)
        self.assertIn('My vote is for choice two.', resp.data)


    ################
    #### models ####
    ################
    
    def test_user_can_vote_and_vote_increases(self):
        pass

if __name__ == "__main__":
    unittest.main()