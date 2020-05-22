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
        self.casting_assistant = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InM4ZkpjejNOQjRMVkFQd2EyQmp2ZSJ9.eyJpc3MiOiJodHRwczovL2lzaGFtcy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVjN2U0ZmRkZDA4MGIwY2I1YWIzMmM5IiwiYXVkIjoiY2Fwc3RvbmVwcm9qIiwiaWF0IjoxNTkwMTU5MTI3LCJleHAiOjE1OTAyNDU1MjcsImF6cCI6Ik1ZZmNCV0JMMW1Ua054ampxV1dvUjRtbVRmZXNZSlZrIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.kFyKzCRzIfn6vMi0wYYK4lk4hFqxHvAQXbK9ruEfwhCqWnAKq3lQftfWuLnJoxmiyPg_CGflYZUt1n6sQ1ez8GdfqJ41upJgI8rV2QePseNgwTDqey2fuXGsiNy8LnryYq_Xv-0pwC6wnLGodj5Ar27fQ8ZhPLxz35BkoEk_-nVFIr7nukrjACXd5lOdT_lEShtQ8_iQHQXCzUBuSbU6lw4kB-bo8zQtJN34OY2TByHMTLUoXEwb6WLPTIzI9HkorJ6AObgTNZUrs0Md8ZdaSp6z22W3toMd4FWbA5KCogrhnjkcQ015OCnzl3Wsj2jjW7iE04loNy_pLty9kLGJ-w"
        self.casting_director = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InM4ZkpjejNOQjRMVkFQd2EyQmp2ZSJ9.eyJpc3MiOiJodHRwczovL2lzaGFtcy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVjN2U1MzczYjM2MDkwY2I4NzZiZWIxIiwiYXVkIjoiY2Fwc3RvbmVwcm9qIiwiaWF0IjoxNTkwMTU5MjQzLCJleHAiOjE1OTAyNDU2NDMsImF6cCI6Ik1ZZmNCV0JMMW1Ua054ampxV1dvUjRtbVRmZXNZSlZrIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInVwZGF0ZTphY3RvcnMiLCJ1cGRhdGU6bW92aWVzIl19.AmIOBMLAf4emQxFhT1xMVnskm4u97IX1h6Lvhk9Hq9aNwapOmaE4m5aiou8MfmGc64bkQt6cF8CsSNvfsQZke2HV-bW_horazSZBldNlvfSn7JnPNCC7FAClpa2t72CQX0vs5gfB5Tik8rCkQrmQMpqbGMn-vjb3X79dGjS3vZuZruL3ZLLt10yRu-mX5ph-Ve24lTgtrMCVZmdEG4EwHycSBYGzReIZ2ctKS8HC90IDxyFiXWKr0mx3gFkGsOuytOu-uk6XRY7MjdWcMqc6ZT_ZcDow8bXp6j1lqDC3OrD4q6CmbselJEWBtKycrVVPgGnZUsq0aAq_RjiS8YctJQ"
        self.executive_producer = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InM4ZkpjejNOQjRMVkFQd2EyQmp2ZSJ9.eyJpc3MiOiJodHRwczovL2lzaGFtcy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVjN2U1MjMzYjM2MDkwY2I4NzZiZTY1IiwiYXVkIjoiY2Fwc3RvbmVwcm9qIiwiaWF0IjoxNTkwMTU5MzQ2LCJleHAiOjE1OTAyNDU3NDYsImF6cCI6Ik1ZZmNCV0JMMW1Ua054ampxV1dvUjRtbVRmZXNZSlZrIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyIsInVwZGF0ZTphY3RvcnMiLCJ1cGRhdGU6bW92aWVzIl19.FJzSEAx2BjR_BQCW_lYf8M5VLzn9zm-zAqbgEt0tbNV2WWbTb3WJ_CCYhujSnTrdkg1rdqOn5CEFP_tiFWmV3A85pG6S4gnehQnGVqYvALX8XHLi-CU0qpphMSAvUjPjjnvEHJn3i9Fmgxcfxesog3jhHaebzxGz3mMR1TsJPmZ8b6omRXoshF9IXh38VlgBfWXb5UAmbKS06oZJrURE0ozjSCFFgDFQK0ivYEaejeWlC3_jGbuUgJjxd-eCWVfQEuE6ksSnOpEca8zUH-zCOqP173c32hZwFY5JyOiotTU81OOaRrqWq3z9GqZoXtop1sSMDWGg1pR1IVTnRc6teg"
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
