from authentication.models import UserProfile
from django.test import TestCase

# Create your tests here.
from voting.models import Voting

from base.tests import BaseTestCase


class List_View_Tests(BaseTestCase):
    fixtures = ['visualizer/migrations/populate.json', ]
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_get_list_voting_200(self):
        response = self.client.get('/visualizer/')
        self.assertEqual(response.status_code, 200)

    def test_get_votings_from_list_voting_anonymous(self):
        response = self.client.get('/visualizer/')
        votings = response.context['votings']
        self.assertEqual(votings, [])
