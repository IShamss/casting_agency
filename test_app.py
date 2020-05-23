import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor


class MoviesTestCase(unittest.TestCase):
    '''
    This class represents the app itself as a whole
    '''

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.casting_assistant = 'JWT here'
        self.executive_producer = 'JWT here'
        self.database_name = "moviesdb"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5433', self.database_name)
        setup_db(self.app, self.database_path)
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    '''Tests for movies
    '''
    # test for retrieving all movies

    def test_get_movies(self):
        res = self.client().get('/movies', headers={
            'Authorization': f'Bearer {self.casting_assistant}'
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_401_get_movie(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # test for creating a new movie
    def test_create_movie(self):
        res = self.client().post('/movies', json={
            'title': 'test movie',
            'release_date': 'test date'
        }, headers={
            'Authorization': f'Bearer {self.executive_producer}'
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['created_movie_id'])
        self.assertTrue(data['created_movie_title'])

    def test_401_create_movie(self):
        res = self.client().post('/movies', json={
            'title': 'test movie',
            'release_date': 'test date'
        }, headers={
            'Authorization': f'Bearer {self.casting_assistant}'
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    # test for editing existing movies
    def test_edit_movie(self):
        res = self.client().patch('/movies/2', json={
            'title': 'test edited title',
            'release_date': '28-05-19 04:55:50 PM'
        }, headers={
            'Authorization': f'Bearer {self.executive_producer}'
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['updated_movie_title'])

    def test_401_edit_movie(self):
        res = self.client().patch('/movies/2', json={
            'title': 'test edited title',
            'release_date': '28-05-19 04:55:50 PM'
        }, headers={
            'Authorization': f'Bearer {self.casting_assistant}'
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_404_edit_movie(self):
        res = self.client().patch('/movies/10000', json={
            'title': 'test edited title',
            'release_date': '28-05-19 04:55:50 PM'
        }, headers={
            'Authorization': f'Bearer {self.executive_producer}'
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    # test for deleting a movie
    def test_delete_movie(self):
        res = self.client().delete('/movies/1', headers={
            'Authorization': f'Bearer {self.executive_producer}'
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['deleted'])

    def test_401_delete_movie(self):
        res = self.client().delete('/movies/1', headers={
            'Authorization': f'Bearer {self.casting_assistant}'
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_404_delete_movie(self):
        res = self.client().delete('/movies/1000', headers={
            'Authorization': f'Bearer {self.executive_producer}'
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    '''
    Tests for the actor routes
    '''
    # getting all actors from the database

    def test_get_actors(self):
        res = self.client().get('/actors', headers={
            'Authorization': f'Bearer {self.casting_assistant}'
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_401_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # test for creating a new actor

    def test_create_actor(self):
        res = self.client().post('/actors', json={
            'name': 'test actor',
            'age': 30,
            'gender': 'Female'
        }, headers={
            'Authorization': f'Bearer {self.casting_director}'
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['created_actor_id'])
        self.assertTrue(data['created_actor_name'])

    def test_401_create_actor(self):
        res = self.client().post('/actors', json={
            'name': 'test actor',
            'age': 30,
            'gender': 'Female'
        }, headers={
            'Authorization': f'Bearer {self.casting_assistant}'
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    # test for editing existing actors

    def test_edit_actor(self):
        res = self.client().patch('/actors/2', json={
            'name': 'test edited actor',
            'age': 34,
            'gender': "Male"
        }, headers={
            'Authorization': f'Bearer {self.executive_producer}'
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['updated_actor_name'])

    def test_401_edit_actor(self):
        res = self.client().patch('/actors/2', json={
            'name': 'test edited actor',
            'age': 34,
            'gender': "Male"
        }, headers={
            'Authorization': f'Bearer {self.casting_assistant}'
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_404_edit_actor(self):
        res = self.client().patch('/actors/10000', json={
            'name': 'test edited actor',
            'age': 55,
            'gender': 'Male'
        }, headers={
            'Authorization': f'Bearer {self.executive_producer}'
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    # test for deleting an actor
    def test_delete_actor(self):
        res = self.client().delete('/actors/3', headers={
            'Authorization': f'Bearer {self.executive_producer}'
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['deleted'])

    def test_401_delete_actor(self):
        res = self.client().delete('/actors/3', headers={
            'Authorization': f'Bearer {self.casting_assistant}'
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_404_delete_actor(self):
        res = self.client().delete('/actors/100', headers={
            'Authorization': f'Bearer {self.executive_producer}'
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
