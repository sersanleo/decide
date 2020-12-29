import random
import itertools
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.db.utils import IntegrityError
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from base import mods
from base.tests import BaseTestCase
from census.models import Census
from mixnet.mixcrypt import ElGamal
from mixnet.mixcrypt import MixCrypt
from mixnet.models import Auth
from voting.models import Voting, Question, QuestionOption
from django.db.utils import IntegrityError
from .admin import give_message

from store.models import Vote


class VotingTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def encrypt_msg(self, msg, v, bits=settings.KEYBITS):
        pk = v.pub_key
        p, g, y = (pk.p, pk.g, pk.y)
        k = MixCrypt(bits=bits)
        k.k = ElGamal.construct((p, g, y))
        return k.encrypt(msg)

    def create_voting(self):
        q = Question(desc='test question', option_types=2)
        q.save()
        for i in range(4):
            opt = QuestionOption(question=q, option='option {}'.format(i+1), rank_order = i+1)
            opt.save()
        v = Voting(name='test voting', question=q)
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v
      
    def create_voting_multi(self):
        q1 = Question(desc='test1 question', option_types=2)
        q2 = Question(desc='test2 question', option_types=2)
        q1.save()
        q2.save()
        for i in range(5):
            opt = QuestionOption(question=q1, option='option {}'.format(i+1))
            opt.save()
        for i in range(5):
            opt = QuestionOption(question=q2, option='option {}'.format(i+1))
            opt.save()
        v = Voting(name='test voting')
        v.save()
        v.question.add(q1)
        v.question.add(q2)

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v

    def create_voters(self, v):
        for i in range(100):
            u, _ = User.objects.get_or_create(username='testvoter{}'.format(i))
            u.is_active = True
            u.save()
            c = Census(voter_id=u.id, voting_id=v.id)
            c.save()

    def get_or_create_user(self, pk):
        user, _ = User.objects.get_or_create(pk=pk)
        user.username = 'user{}'.format(pk)
        user.set_password('qwerty')
        user.save()
        return user


    def store_votes_unique_option(self, v):
        voters = list(Census.objects.filter(voting_id=v.id))
        voter = voters.pop()

        clear = {}
        for i in range(3):
            main_voter = self.get_or_create_user(voter.voter_id)
            self.login(user=main_voter.username)
            votos = []
            
            options = v.question.options.all()
            count_options = len(options)
            for j in range(1):
                chosen_option = options[random.randint(0, count_options-1)]
                
                if chosen_option.number in clear:
                    clear[chosen_option.number] += 1
                else:
                    clear[chosen_option.number] = 1

                a, b = self.encrypt_msg(chosen_option.number, v)
                votos.append({ 'a': a, 'b': b })
            
            data = {
                'voting': v.id,
                'voter': voter.voter_id,
                'votes': votos,
            }                

            mods.post('store', json=data)
            voter = voters.pop()
        return clear

    def test_complete_unique_option_voting(self):
        v = self.create_voting()
        self.create_voters(v)

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        clear = self.store_votes_unique_option(v)

        self.login()  # set token
        v.tally_votes(self.token)

        tally = v.tally
        message=give_message(v)
        self.assertIn("For voting:test voting", message)
        tally.sort()
        tally = {k: len(list(x)) for k, x in itertools.groupby(tally)}

        for q in v.question.options.all():
            self.assertEqual(tally.get(q.number, 0), clear.get(q.number, 0))

        for q in v.postproc:
            self.assertEqual(tally.get(q["number"], 0), q["votes"])


    def store_votes_multiple_option(self, v):
        voters = list(Census.objects.filter(voting_id=v.id))
        voter = voters.pop()

        clear = {}
        for i in range(3):
            main_voter = self.get_or_create_user(voter.voter_id)
            self.login(user=main_voter.username)
            votos = []
            
            options = v.question.options.all()
            count_options = len(options)
            for j in range(count_options):
                chosen_option = options[j]
                
                if chosen_option.number in clear:
                    clear[chosen_option.number] += 1
                else:
                    clear[chosen_option.number] = 1

                a, b = self.encrypt_msg(chosen_option.number, v)
                votos.append({ 'a': a, 'b': b })
            
            data = {
                'voting': v.id,
                'voter': voter.voter_id,
                'votes': votos,
            }                

            mods.post('store', json=data)
            voter = voters.pop()
        return clear

    def test_complete_multiple_option_voting(self):
        v = self.create_voting()
        self.create_voters(v)

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        clear = self.store_votes_multiple_option(v)

        self.login()  # set token
        v.tally_votes(self.token)
        tally = v.tally
        message=give_message(v)
        self.assertIn("For voting:test voting", message)
        tally.sort()
        tally = {k: len(list(x)) for k, x in itertools.groupby(tally)}

        for q in v.question.options.all():
            self.assertEqual(tally.get(q.number, 0), clear.get(q.number, 0))

        for q in v.postproc:
            self.assertEqual(tally.get(q["number"], 0), q["votes"])


    def store_votes_ranked_option(self, v):
        voters = list(Census.objects.filter(voting_id=v.id))
        voter = voters.pop()

        clear = {}
        for i in range(3):
            main_voter = self.get_or_create_user(voter.voter_id)
            self.login(user=main_voter.username)
            votos = []
            
            options = v.question.options.all()
            count_options = len(options)
            for j in range(count_options):
                chosen_option = options[j]
                
                if chosen_option.number in clear:
                    clear[chosen_option.number] += 1
                else:
                    clear[chosen_option.number] = 1

                a, b = self.encrypt_msg(chosen_option.number, v)
                c, d = self.encrypt_msg(chosen_option.rank_order, v)
                votos.append({ 'a': a, 'b': b, 'c': c, 'd': d })
            
            data = {
                'voting': v.id,
                'voter': voter.voter_id,
                'votes': votos,
            }                

            mods.post('store', json=data)
            voter = voters.pop()
        return clear

    def test_complete_ranked_option_voting(self):
        v = self.create_voting()
        self.create_voters(v)

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        clear = self.store_votes_ranked_option(v)

        self.login()  # set token
        v.tally_votes(self.token)
        tally = v.tally
        message=give_message(v)
        self.assertIn("For voting:test voting", message)
        tally.sort()
        tally = {k: len(list(x)) for k, x in itertools.groupby(tally)}

        for q in v.question.options.all():
            self.assertEqual(tally.get(q.number, 0), clear.get(q.number, 0))

        for q in v.postproc:
            self.assertEqual(tally.get(q["number"], 0), q["votes"])


    def test_create_voting_from_api(self):
        data = {'name': 'Example'}
        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 400)

        data = {
            'name': 'Example',
            'desc': 'Description example',
            'question': 'I want a ',
            'question_opt': ['cat', 'dog', 'horse']
        }

        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 201)


    def create_question(self):
        q = Question(desc='test question')
        q.save()
        return q

    def test_question_unique(self):
        v = self.create_question()
        with self.assertRaises(Exception) as raised:
            self.create_question()
        self.assertEqual(IntegrityError, type(raised.exception))

    def test_duplicate_voting_name(self):
        v1 = self.create_voting()
        with self.assertRaises(Exception) as raised:
            v2 = self.create_voting()
        self.assertEqual(IntegrityError, type(raised.exception))
        
    def test_multi_voting(self):
        v1 = self.create_voting_multi()
        print(v1.question)

  