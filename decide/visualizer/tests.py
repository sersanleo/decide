from django.test import TestCase
from base.tests import BaseTestCase
# Create your tests here.

class Statistics_View_Tests(BaseTestCase):
    fixtures = ['visualizer/migrations/populate.json', ]

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_get_detail_voting_20(self):
        response = self.client.get('/visualizer/20/statistics')
        self.assertEqual(response.status_code, 200)

    def test_get_detail_voting_21(self):
        response = self.client.get('/visualizer/21/statistics')
        self.assertEqual(response.status_code, 200)

    def test_get_detail_voting_22(self):
        response = self.client.get('/visualizer/22/statistics')
        self.assertEqual(response.status_code, 200)

    def test_get_detail_voting_404(self):
        response = self.client.get('/visualizer/10/statistics')
        self.assertEqual(response.status_code, 404)