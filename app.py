import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Movie, Actor, setup_db

from auth import AuthError, requires_auth


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

def create_app(test_config=None):

    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization, true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, PUT, POST, DELETE, OPTIONS'
        )
        return response

    setup_db(app)

    @app.route('/')
    def welcome():
        """
            Welcome
        """

        return jsonify({
            'success': True,
            'message': "welcome to capstone"
        }), 200

    #  Movies
    #  ----------------------------------------------------------------

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(payload):
        """
            Gets all Movies
        """

        query = Movie.query.order_by(Movie.id).all()
        data = [movie.format() for movie in query]

        return jsonify({
            'success': True,
            'all_movies': data
        }), 200

    @app.route('/movies/add', methods=['POST'])
    @requires_auth('add:movies')
    def create_movies(payload):
        """
        Creates a new movie
        """

        request_data = request.get_json()

        title = request_data.get('title')
        description = request_data.get('description')
        category = request_data.get('category')

        if title is None:
            abort(422)

        new_movie = Movie(
            title=title,
            description=description,
            category=category
        )

        Movie.insert(new_movie)

        return jsonify({
            'success': True,
            'message': 'the movie ' + title + ' was successfully listed',
            'movie': new_movie.format()
        }), 201

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        """
            Deletes a movie by ID
        """

        movie = Movie.query.get(movie_id)

        if not movie:
            abort(404)
        title = movie.title
        Movie.delete(movie)

        return jsonify({
            "success": True,
            'message': 'Movie ' + title + ' successfully deleted.'
        }), 200

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, movie_id):
        """
            Updates movie title
        """
        request_data = request.get_json()
        movie = Movie.query.get(movie_id)

        if not movie:
            abort(404)
        setattr(movie, 'title', request_data['title'])
        if 'description' in request_data:
            description = request_data['description']
            setattr(movie, 'description', description)
        if 'category' in request_data:
            category = request_data['category']
            setattr(movie, 'category', category)

        Movie.update(movie)

        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200

    #  Actors
    #  ----------------------------------------------------------------

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(payload):
        """
            Gets all actors
        """

        query = Actor.query.order_by(Actor.id).all()
        data = [actor.format() for actor in query]

        return jsonify({
            'success': True,
            'all_actors': data
        }), 200

    @app.route('/actors/add', methods=['POST'])
    @requires_auth('add:actors')
    def create_actor(payload):
        """
        Creates a new actor
        """

        request_data = request.get_json()

        name = request_data.get('name')
        age = request_data.get('age')
        gender = request_data.get('gender')

        new_actor = Actor(
            name=name,
            age=age,
            gender=gender
        )

        Actor.insert(new_actor)

        return jsonify({
            'success': True,
            'message': 'Actor was successfully listed',
            'actor': new_actor.format()
        }), 201

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        """
            Deletes a actor by ID
        """

        actor = Actor.query.get(actor_id)

        if not actor:
            abort(404)
        name = actor.name

        Actor.delete(actor)

        return jsonify({
            "success": True,
            'message': 'Actor ' + name + ' successfully deleted.'
        }), 200

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload, actor_id):
        """
            Updates an actor
        """
        request_data = request.get_json()
        actor = Actor.query.get(actor_id)

        if not actor:
            abort(404)

        actor.name = request_data.get("name", actor.name)
        actor.age = request_data.get("age", actor.age)
        setattr(actor, 'gender', request_data['gender'])

        Actor.update(actor)

        return jsonify({
            'success': True,
            'actor': actor.format()
        }), 200

    # ----------------------------------------------------------------------------#
    # Error Handling.
    # ----------------------------------------------------------------------------#

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Request"
        }), 422

    @app.errorhandler(401)
    def not_authorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized"
        }), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found"
        }), 404

    @app.errorhandler(403)
    def permission_error(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Unauthorized"
        }), 403

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify(error.error), error.status_code

    return app


# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#
app = create_app()

# specify port manually:
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
