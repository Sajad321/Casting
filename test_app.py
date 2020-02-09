import os
import unittest
import json
import random
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie


TEST_DATABASE_URI = os.getenv('TEST_DATABASE_URI')
CASTING_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFVSTVNRFpCUmtFM05UQkNNakE1TVVJM1JFTTBOVGhDUkRNME4wUkJRVFZCT1VNNU5qWXlNZyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRjNy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWUyYWY1NzRlNjljMmUwZThlNTdkNWY1IiwiYXVkIjoiQ29mZmVlIiwiaWF0IjoxNTgxMTkwNDE5LCJleHAiOjE1ODEyNzY4MTksImF6cCI6Imh5OGdsWHljVjdBRmRuMlJ5UU1ta2oxQmxpR3NmTFFVIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6ZHJpbmtzIiwiZ2V0OmFjdG9ycyIsImdldDpkcmlua3MtZGV0YWlsIiwiZ2V0Om1vdmllcyIsInBhdGNoOmRyaW5rcyIsInBvc3Q6ZHJpbmtzIl19.dVpzQJAObVjU36qhJguJAYcr8ZlnuYEWJUS8El6bp6aFBNSr9yPVil2_gL6MO_c5TXXCn-yxDZtdhis2xKzCJlVvWoTqQlbNMjvsnE3R85le3xzEThERQMXc2SiptS6YP3y5IMw07fcnKRqRBMZM7eCdmCsCq6atri4IauPNq7Qeo-8X6qjG2iDAdexZhdVB4ny6xijkbX59HWvHkKUfCa53jAsz4MK1k74xEl7m-JfTryiywPAidkkOJBz4JErw7wy7XchTAUcS8ZNIAbjQjqdgKbC-e42c3SEcXMN-UDVPXAKT-bxZdGYvWI5vnjzobi4TBdY_E3fPwv5JzagHOA'
CASTING_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFVSTVNRFpCUmtFM05UQkNNakE1TVVJM1JFTTBOVGhDUkRNME4wUkJRVFZCT1VNNU5qWXlNZyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRjNy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWUyYjNlODg2NTI1NWQwZTljMWVlNzRhIiwiYXVkIjoiQ29mZmVlIiwiaWF0IjoxNTgxMTkwNTUyLCJleHAiOjE1ODEyNzY5NTIsImF6cCI6Imh5OGdsWHljVjdBRmRuMlJ5UU1ta2oxQmxpR3NmTFFVIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJhZGQ6YWN0b3JzIiwiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6ZHJpbmtzLWRldGFpbCIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiXX0.EE7wLQEKoT93DhE5dJW-Tl69wrEmyA3zw3mbHOF2NRR13clb-8znQBWtgmFbjwL3Er6w2QENGNXdjcuwMRdiHpfQ8M4-J_jxPBw4mEe-Cp9doAyavbLgmNBy1Jm_m2G1RRLXVCiM1bCSslQ32arZMoCVUNFUUwXc-Q7cJtn5saHmg_SF8_-6nPYj-dMUJhjUT09w-QiVt95gIkO-w-9zRgBU7rkFAjw1K8t0JxVg6l4HtjEEK3x3ptk2NZDpNlDmUPzDfZhux_gWtqKY4W8UJ7LCqhGCfxYNTakYSQVOKdGHuVnvTHKJM10d60uWWEqdyoJTlxZlU0OflLDlU1Aufg'
EXECUTIVE_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFVSTVNRFpCUmtFM05UQkNNakE1TVVJM1JFTTBOVGhDUkRNME4wUkJRVFZCT1VNNU5qWXlNZyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRjNy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWUzZWZlN2E4Yjk0ZTQwZWNlY2U5NjRmIiwiYXVkIjoiQ29mZmVlIiwiaWF0IjoxNTgxMTkwNjM5LCJleHAiOjE1ODEyNzcwMzksImF6cCI6Imh5OGdsWHljVjdBRmRuMlJ5UU1ta2oxQmxpR3NmTFFVIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJhZGQ6YWN0b3JzIiwiYWRkOm1vdmllcyIsImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiXX0.WJ5gWlKMfqbZFZH2TVhCntcjf4YgPgGKGRKCe7hE4ThSTRMOiPLxKwezLwfMsibGn_lMnAzPK_tqBI7cCmYLIpvJhsMVmUruwgA14-Hbks_IMK8_wdn6KACKNMEFKHr3SaZ4NDSOiIC4Fhq7jY21mjHdrvMQcx7Sc8UFePWDx42-jkXGhq_tQHNv7KaDUfYIPWOqEQq6YYEYF70Fw_18yuTCNoH1xe_5iZ878kAl2nx552yIoI4m06cVWBaC25x2C14svc8dlESoGNL1sKUymBrfgAHJWFrC9UTJdMa4RmS1tsKk7DAME8dszyJxDGKYKDHzoulOUYtz--J1QVCKlQ'

# CASTING_ASSISTANT is CA
# CASTING_DIRECTOR is CD
# EXECUTIVE_PRODUCER is EP


class CastingAgencyTest(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.casting_assistant = CASTING_ASSISTANT
        self.casting_director = CASTING_DIRECTOR
        self.executive_producer = EXECUTIVE_PRODUCER
        setup_db(self.app, TEST_DATABASE_URI)
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

    '''
    RBAC TEST
    '''

    def test_post_actors_by_EP_with_auth_201(self):
        response = self.client().post('/actors/add',
                                      headers={
                                          "Authorization": "Bearer {}"
                                          .format(self.executive_producer)
                                      },
                                      json={
                                          "name": "Edward",
                                          "gender": "male",
                                          "age": 25,
                                      })
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(data['actor'])

    def test_post_actors_by_CA_without_auth_403(self):
        response = self.client().post('/actors/add',
                                      headers={
                                          "Authorization": "Bearer {}"
                                          .format(self.casting_assistant)
                                      },
                                      json={
                                          "name": "Edward",
                                          "gender": "male",
                                          "age": 25
                                      })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')

    def test_post_movies_by_EP_with_auth_201(self):
        response = self.client().post('/movies/add',
                                      headers={
                                          "Authorization": "Bearer {}"
                                          .format(self.executive_producer)
                                      },
                                      json={
                                          "title": "Iron Man",
                                          "release_date": "2015-01-01"
                                      })

        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(data['movie'])

    def test_post_movies_by_CA_without_auth_403(self):
        response = self.client().post('/movies/add',
                                      headers={
                                          "Authorization": "Bearer {}"
                                          .format(self.casting_assistant)
                                      },
                                      json={
                                          "title": "Iron Man",
                                          "release_date": "2015-01-01"
                                      })

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')

    def test_get_actors_by_CA_with_auth_200(self):
        response = self.client().get('/actors',
                                     headers={
                                         "Authorization": "Bearer {}"
                                         .format(self.casting_assistant)
                                     })
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['all_actors'])

    def test_get_actors_by_CA_without_auth_401(self):
        response = self.client().get('/actors')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')

    def test_get_movies_by_CA_with_auth_200(self):
        response = self.client().get('/movies',
                                     headers={
                                         "Authorization": "Bearer {}"
                                         .format(self.casting_assistant)
                                     })
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['all_movies'])

    def test_get_movies_by_CA_without_auth_401(self):
        response = self.client().get('/movies')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')

    def test_patch_actors_by_CD_with_auth_200(self):
        random_id = random.choice([actor.id for actor in Actor.query.all()])
        response = self.client().patch('/actors/{}'.format(random_id),
                                       headers={
            "Authorization": "Bearer {}".format(self.casting_director)
        },
            json={
            "name": "David",
            "gender": "other",
            "age": 10
        })

        data = json.loads(response.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['actor'])

    def test_patch_actors_by_CA_without_auth_403(self):
        random_id = random.choice([actor.id for actor in Actor.query.all()])
        response = self.client().patch('/actors/{}'.format(random_id),
                                       headers={
            "Authorization": "Bearer {}".format(self.casting_assistant)
        },
            json={
            "name": "David",
            "gender": "other",
            "age": 10
        })

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')

    def test_patch_movies_by_CD_with_auth_200(self):
        random_id = random.choice([movie.id for movie in Movie.query.all()])
        response = self.client().patch('/movies/{}'.format(random_id),
                                       headers={
            "Authorization": "Bearer {}".format(self.casting_director)
        },
            json={
            "title": "Joker",
            "release_date": "2019-10-1"
        })

        data = json.loads(response.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['movie'])

    def test_patch_movies_by_CA_without_auth_403(self):
        random_id = random.choice([movie.id for movie in Movie.query.all()])
        response = self.client().patch('/movies/{}'.format(random_id),
                                       headers={
            "Authorization": "Bearer {}".format(self.casting_assistant)
        },
            json={
            "title": "Joker",
            "release_date": "2019-10-1"
        })

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')

    def test_delete_actors_by_EP_with_auth_200(self):
        random_id = random.choice([actor.id for actor in Actor.query.all()])
        response = self.client().delete('actors/{}'.format(random_id),
                                        headers={
                                            "Authorization": "Bearer {}"
                                            .format(self.executive_producer)
        }
        )
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['message'])

    def test_delete_actors_by_CA_without_auth_403(self):
        random_id = random.choice([actor.id for actor in Actor.query.all()])
        response = self.client().delete('actors/{}'.format(random_id),
                                        headers={
                                            "Authorization": "Bearer {}"
                                            .format(self.casting_assistant)
        }
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')

    def test_delete_movies_by_EP_with_auth_200(self):
        random_id = random.choice([movie.id for movie in Movie.query.all()])
        response = self.client().delete('movies/{}'.format(random_id),
                                        headers={
                                            "Authorization": "Bearer {}"
                                            .format(self.executive_producer)
        }
        )
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['message'])

    def test_delete_movies_by_CA_without_auth_403(self):
        random_id = random.choice([movie.id for movie in Movie.query.all()])
        response = self.client().delete('movies/{}'.format(random_id),
                                        headers={
                                            "Authorization": "Bearer {}"
                                            .format(self.casting_assistant)
        }
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')


if __name__ == '__main__':
    unittest.main()
