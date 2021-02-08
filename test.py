from unittest import TestCase
from app import app
from flask import session, request, jsonify
from boggle import Boggle
import simplejson as json


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

    def test_boggle_home(self):
        """"test everything loads correctly at start"""
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text = True)
            self.assertIn('td', html)
            self.assertIn('input', html)
            self.assertIn('Submit', html)
            self.assertIn('score', html)
            self.assertEqual(res.status_code, 200)
    
    def test_submit_guess(self):
        """tests variety of cases for submitting guesses with only A on the board"""
        
        # test for ok response
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                board = [['A','A','A','A','A'], ['A','A','A','A','A'], ['A','A','A','A','A'], ['A','A','A','A','A'], ['A','A','A','A','A']]
                change_session['board'] = board
            res = client.get('/submit?word=a')
            self.assertEqual(res.status_code, 200)
            self.assertIn("ok", res.data.decode('utf-8'))

            # test for not on board response
            with client.session_transaction() as change_session:
                board = [['A','A','A','A','A'], ['A','A','A','A','A'], ['A','A','A','A','A'], ['A','A','A','A','A'], ['A','A','A','A','A']]
                change_session['board'] = board
            res = client.get('/submit?word=add')
            self.assertEqual(res.status_code, 200)
            self.assertIn("not-on-board", res.data.decode('utf-8'))

           # test for not word response
            with client.session_transaction() as change_session:
                board = [['A','A','A','A','A'], ['A','A','A','A','A'], ['A','A','A','A','A'], ['A','A','A','A','A'], ['A','A','A','A','A']]
                change_session['board'] = board
            res = client.get('/submit?word=aasdfasdf')
            self.assertEqual(res.status_code, 200)
            self.assertIn("not-word", res.data.decode('utf-8'))
           
    def test_game_over(self):
        """test that new high score updates high score,
         test that lower score than high score doesnt update high score
        and test that each game over increases the times session by 1"""
        with app.test_client() as client:
            res = client.post('/game-over', json={ 'score': 1 })
            self.assertEqual(session['times'], 1)
            self.assertEqual(session['highscore'], 1)
            self.assertEqual(res.data.decode('utf-8'), 'done')

            res = client.post('/game-over', json={ 'score': 0 })
            self.assertEqual(session['times'], 2)
            self.assertEqual(session['highscore'], 1)
            self.assertEqual(res.data.decode('utf-8'), 'done')