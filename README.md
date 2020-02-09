## Full Stack Casting Agency API Backend

# Casting Agency Specifications

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

# Motivation for project

This is the final project for Udacity fullstack nanodegree program, which applies the skillset of using Flask, SQLAlchemy, Auth0, gunicorn and heroku to develop and deploy a RESTful API, To get a fully functional ready backend app.

# Getting Started
Installing Dependencies
Python 3.6
Follow instructions to install the latest version of python for your platform in the python docs

# Virtual Enviornment
We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the python docs

# PIP Dependencies
Once you have your virtual environment setup and running, install dependencies by running:

`pip install -r requirements.txt`
This will install all of the required packages we selected within the requirements.txt file.

# Key Dependencies
- Flask is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- SQLAlchemy is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- Flask-CORS is the extension we'll use to handle cross origin requests from our frontend server.
- Flask-Migrate is the extension we'll use to handle migration and modifying of the database
- jose JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

# Database Setup
To test endpoints, with Postgres running, just add elements to the database

# Running the server
From within the file directory first ensure you are working using your created virtual environment.

To run the server, execute:

`python app.py`

Setting the FLASK_ENV variable to development will detect file changes and restart the server automatically.

# Tasks
1. Setup Auth0
2. Create a new Auth0 Account
3. Select a unique tenant domain
4. Create a new, single page web application
5. Create a new API
    in API Settings:
    Enable RBAC
    Enable Add Permissions in the Access Token
    Create new API permissions:
        - add:actors
        - add:movies
        - delete:actors
        - delete:movies
        - patch:actors
        - patch:movies
        - get:actors
        - get:movies
6. Create new roles for:
    Casting Assistant
        Can view actors and movies`
    Casting Director
        All permissions a Casting Assistant has and ...
        Add or delete an actor from the database
        Modify actors or movies
    Executive Producer
        All permissions a Casting Director has and ...
    Add or delete a movie from the database
7. Test your endpoints with `test_app.py`.
8. Register 3 users - assign the Casting Assistant role to one and Casting Director role to another, and Executive Producer to the other.
9. Sign into each account and make note of the JWT.
10. Test each endpoint and correct any errors.

# Demo Page
https://casting1234.herokuapp.com/


# Endpoints documentation
GET `/movies`
    - Fetches a dictionary of movies
Returns: Returns Json data about movies
Success Response:
```
{
    "all_movies": [
        {
            "id": 1,
            "release_date": "Sun, 01 Jan 2012 00:00:00 GMT",
            "title": "Lion King"
        },
        {
            "id": 2,
            "release_date": "Mon, 12 Aug 2019 00:00:00 GMT",
            "title": "Joker"
        },
        {
            "id": 3,
            "release_date": "Mon, 12 Dec 2011 00:00:00 GMT",
            "title": "Frozen"
        },
        {
            "id": 4,
            "release_date": "Wed, 01 Aug 2012 00:00:00 GMT",
            "title": "Yes Man"
        }
    ],
    "status_code": 200,
    "success": true
}
```
GET `/actors`
    - Fetches a dictionary of actors
Returns: Json data about actors
Success Response:
```
  {
    "all_actors": [
        {
            "age": 36,
            "gender": "male",
            "id": 1,
            "name": "Edward"
        },
        {
            "age": 25,
            "gender": "other",
            "id": 2,
            "name": "David"
        },
        {
            "age": 35,
            "gender": "female",
            "id": 3,
            "name": "Jeff"
        }
    ],
    "status_code": 200,
    "success": true
}
```
DELETE `/movies/<int:movie_id>`
    - Deletes the movie_id of movie
    - Required URL Arguments: movie_id: movie_id_integer
Returns: Json data about the deleted movie's ID
Success Response:
```
{
    "status_code": 200,
    'message': 'Movie ' + title + ' successfully deleted.',
    "success": true
}
```
DELETE `/actors/<int:actor_id>`
    - Deletes the actor_id of actor
    - Required URL Arguments: actor_id: actor_id_integer
Returns: Json data about the deleted actor's ID
Success Response:
```
{
    "status_code": 200,
    'message': 'Actor ' + name + ' successfully deleted.'
    "success": true
}
```
POST `/movies/add`
    - Post a new movie in a database.
    - Required Data Arguments: Json data
Success Response:
```
{
    "movie": {
        "id": 6,
        "release_date": "Thu, 01 Aug 2002 00:00:00 GMT",
        "title": "Toy Story"
    },
    "status_code": 201,
    'message': 'the movie ' + title + ' was successfully listed',
    "success": true
}
```
POST `/actors/add`
    - Post a new actor in a database.
    - Required Data Arguments: Json data
Success Response:
```
{
    "actor": {
        "age": 18,
        "gender": "other",
        "id": 4,
        "name": "Penny"
    },
    "status_code": 201,
    "message": "Actor was successfully listed",
    "success": true
}
```
PATCH `/movies/<int:movie_id>`
    - Updates the movie_id of movie
    - Required URL Arguments: movie_id: movie_id_integer
Returns: Json data about the updated movie
Success Response:
```
{
    "movie": {
        "id": 5,
        "release_date": "Wed, 05 Dec 2018 00:00:00 GMT",
        "title": "Avenger"
    },
    "status_code": 200,
    "success": true
}
```
PATCH `/actors/<int:actor_id>`
    - Updates the actor_id of actor
    - Required URL Arguments: actor_id: actor_id_integer
Returns: Json data about the deleted actor's ID
Success Response:
```
{
    "actor": {
        "age": 28,
        "gender": "other",
        "id": 4,
        "name": "Penny"
    },
    "status_code": 200,
    "success": true
}
```
# Testing
For testing, required jwts are included for each role. To run the tests, run

`python test_app.py`