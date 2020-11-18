
# Create your tests here.

from django.contrib.auth.models import User
from django.test import Client, TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
import json

from seminar.models import InstructorProfile, ParticipantProfile


class GetUserTestCase(TestCase):
    client = Client()

    def setUp(self):
        self.client.post(
            '/api/v1/user/',
            json.dumps({
                "username": "davin111",
                "password": "password",
                "first_name": "Davin",
                "last_name": "Byeon",
                "email": "bdv111@snu.ac.kr",
                "role": "participant",
                "university": "서울대학교"
            }),
            content_type='application/json'
        )

    def test_get_user_incomplete_request(self):
        response = self.client.get(
            '/api/v1/user/me/',


        )

class PostParticipantTestCase(TestCase):
    client = Client()

    def setUp(self):

        self.client.post(
            'api/v1/user/participant/',
            json.dumps({
                "user": "swl",
                "university": "snu",
                "accepted": 1,

            }),

            context_type = 'application/json'
        )


class PostSeminarTestCase(TestCase):
    client = Client()

    def setUp(self):
        self.client.post(
            '/api/v1/seminar/',
            json.dumps({
                "name": "android",
                "capacity": 60,
                "count": 1,
                "online": 1,


            }),
            content_type='application/json'
        )



class PutSeminarTestCase(TestCase):
    client = Client()

    def setUp(self):
        self.client.put(
            '/api/vi/seminar/{seminar_id}/',

            json.dumps({
                "name": "android",
                "capacity": 60,
                "count": 1,
                "online": 1,

            }),
            content_type = 'application/json'

        )

