import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor, Association
from auth import requires_auth, AuthError


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app, resources={r"*": {"origins": "*"}})
    setup_db(app)

    '''#######################################
  Adding headers for the response
  '''
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,PATCH')
        return response

    ''' #########################################
  Routes
  '''

    # First the movies routes
    # fetch all movies in the database
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def fetch_movies(token):
        try:

            selection = Movie.query.all()
            movies = [movie.format() for movie in selection]
            return jsonify({
                'success': True,
                'movies': movies,
            })
        except BaseException:
            abort(404)
    # create a new movie
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(token):
        body = request.get_json()
        if not body:
            abort(404)
        new_title = body.get('title')
        new_release_date = body.get('release_date')
        new_movie = Movie(title=new_title, release_date=new_release_date)
        new_movie.insert()
        return jsonify({
            'success': True,
            'created_movie_id': new_movie.id,
            'created_movie_title': new_movie.title
        })

    # update an existing movie
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('update:movies')
    def update_movie(token, movie_id):
        body = request.get_json()
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if not body or not movie:
            abort(404)
        new_title = body.get('title')
        new_release_date = body.get('release_date')
        movie.title = new_title
        movie.release_date = new_release_date
        movie.update()
        return jsonify({
            'success': True,
            'updated_movie_title': new_title
        })

    # Delete an existing movie
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(token, movie_id):

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if not movie:
            abort(404)
        movie.delete()
        return jsonify({
            'success': True,
            'deleted': movie_id
        })

    ''' ###################################
  Actor Routes
  '''
    # get all actors in the database
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(token):
        selection = Actor.query.all()
        actors = [actor.format() for actor in selection]
        return jsonify({
            'success': True,
            'actors': actors
        })

    # Create a new actor in the database
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(token):
        body = request.get_json()
        if not body:
            abort(404)
        new_name = body.get('name')
        new_age = body.get('age')
        new_gender = body.get('gender')
        actor = Actor(name=new_name, age=new_age, gender=new_gender)
        actor.insert()
        return jsonify({
            'success': True,
            'created_actor_id': actor.id,
            'created_actor_name': new_name
        })

    # update an existing actor in the database
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('update:actors')
    def update_actor(token, actor_id):
        body = request.get_json()
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if not body or not actor:
            abort(404)
        actor.name = body.get('name')
        actor.age = body.get('age')
        actor.gender = body.get('gender')
        actor.update()
        return jsonify({
            'success': True,
            'updated_actor_name': actor.name
        })

    # delete an actor in the database
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(token, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if not actor:
            abort(404)
        actor.delete()
        return jsonify({
            'success': True,
            'deleted': actor_id
        })

    '''###########################################
  Error Handling
  '''
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': 'Unauthorized'
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'success': False,
            'error': 403,
            'message': 'Forbidden'
        })
    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
