from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms

from base import mods
from base.models import Auth, Key


class Question(models.Model):
    ANSWER_TYPES = ((1, "Unique option"), (2,"Multiple option"), (3,"Rank order scale"))
    option_types = models.PositiveIntegerField(choices=ANSWER_TYPES, default="1")
    desc = models.TextField(unique=True)
    points = models.PositiveIntegerField(default="1")


    def __str__(self):
        return self.desc


class QuestionOption(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    number = models.PositiveIntegerField(blank=True, null=True)
    option = models.CharField(max_length=200)
    rank_order = models.PositiveIntegerField(blank=True, null=True)

    def save(self):
        if not self.number:
            self.number = self.question.options.count() + 2
        return super().save()

    def __str__(self):
        return '{} ({})'.format(self.option, self.number)

class TypeVoting(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return self.name
    
class Voting(models.Model):
    name = models.CharField(max_length=200, unique = True)
    desc = models.TextField(blank=True, null=True)
    question =  models.ManyToManyField(Question, related_name='voting')

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    started_by = models.CharField(max_length=200, blank=True, null = True)

    pub_key = models.OneToOneField(Key, related_name='voting', blank=True, null=True, on_delete=models.SET_NULL)
    auths = models.ManyToManyField(Auth, related_name='votings')

    tally = JSONField(blank=True, null=True)
    tallyM = JSONField(blank=True, null=True)
    tallyF = JSONField(blank=True, null=True)
    postproc = JSONField(blank=True, null=True)
    
    type = models.ForeignKey(TypeVoting, related_name='voting', on_delete=models.CASCADE)

    def create_pubkey(self):
        if self.pub_key or not self.auths.count():
            return

        auth = self.auths.first()
        data = {
            "voting": self.id,
            "auths": [ {"name": a.name, "url": a.url} for a in self.auths.all() ],
        }
        key = mods.post('mixnet', baseurl=auth.url, json=data)
        pk = Key(p=key["p"], g=key["g"], y=key["y"])
        pk.save()
        self.pub_key = pk
        self.save()

    def get_votes(self, token=''):
        # gettings votes from store
        votes = mods.get('store', params={'voting_id': self.id}, HTTP_AUTHORIZATION='Token ' + token)
        # anon votes
        return [[i['a'], i['b']] for i in votes], [[i['c'], i['d']] for i in votes]
    
    def get_votes_masc(self, token=''):
        # gettings votes from store
        votes = mods.get('store', params={'voting_id': self.id}, HTTP_AUTHORIZATION='Token ' + token)
        # anon votes
        return [[i['a'], i['b']] for i in votes if i['sex'] == 'M']

    def get_votes_fem(self, token=''):
        # gettings votes from store
        votes = mods.get('store', params={'voting_id': self.id}, HTTP_AUTHORIZATION='Token ' + token)
        # anon votes
        return [[i['a'], i['b']] for i in votes if i['sex'] == 'F']
    
    def get_info(self,token=''):
        votos=Voting.objects.get(id=self.id)
        return votos
    
    def tally_votes(self, token=''):
        '''
        The tally is a shuffle and then a decrypt
        '''

        votes, ranked_votes = self.get_votes(token)

        auth = self.auths.first()
        shuffle_url = "/shuffle/{}/".format(self.id)
        decrypt_url = "/decrypt/{}/".format(self.id)
        auths = [{"name": a.name, "url": a.url} for a in self.auths.all()]

        data = { "msgs": votes }
        response = mods.post('mixnet', entry_point=shuffle_url, baseurl=auth.url, json=data,
                response=True)
        if response.status_code != 200:
            # TODO: manage error
            pass

        data = {"msgs": response.json()}
        response = mods.post('mixnet', entry_point=decrypt_url, baseurl=auth.url, json=data,
                response=True)

        if response.status_code != 200:
            # TODO: manage error
            pass

        self.tally = response.json()

        if ranked_votes and len(ranked_votes[0]) != 0 and ranked_votes[0][0] != 0:
                    
            data = { "msgs": ranked_votes }
            response = mods.post('mixnet', entry_point=shuffle_url, baseurl=auth.url, json=data,
                    response=True)
            if response.status_code != 200:
                pass

            data = {"msgs": response.json()}
            response = mods.post('mixnet', entry_point=decrypt_url, baseurl=auth.url, json=data,
                    response=True)

            if response.status_code != 200:
                pass

            self.tally = [self.tally, response.json()]

        self.save()

        self.tally_votes_masc(token)
        self.votes_info_opciones()
        self.votes_info_votos()

def tally_votes_masc(self, token=''):
        '''
        The tally is a shuffle and then a decrypt
        '''

        votes = self.get_votes_masc(token)
        
        auth = self.auths.first()
        shuffle_url = "/shuffle/{}/".format(self.id)
        decrypt_url = "/decrypt/{}/".format(self.id)
        auths = [{"name": a.name, "url": a.url} for a in self.auths.all()]

        # first, we do the shuffle
        data = { "msgs": votes }
        response = mods.post('mixnet', entry_point=shuffle_url, baseurl=auth.url, json=data,
                response=True)
        if response.status_code != 200:
            # TODO: manage error
            pass

        # then, we can decrypt that
        data = {"msgs": response.json()}
        response = mods.post('mixnet', entry_point=decrypt_url, baseurl=auth.url, json=data,
                response=True)

        if response.status_code != 200:
            # TODO: manage error
            pass

        self.tallyM = response.json()
        self.save()

        self.tally_votes_fem(token)

    def tally_votes_fem(self, token=''):
        '''
        The tally is a shuffle and then a decrypt
        '''

        votes = self.get_votes_fem(token)
        
        auth = self.auths.first()
        shuffle_url = "/shuffle/{}/".format(self.id)
        decrypt_url = "/decrypt/{}/".format(self.id)
        auths = [{"name": a.name, "url": a.url} for a in self.auths.all()]

        # first, we do the shuffle
        data = { "msgs": votes }
        response = mods.post('mixnet', entry_point=shuffle_url, baseurl=auth.url, json=data,
                response=True)
        if response.status_code != 200:
            # TODO: manage error
            pass

        # then, we can decrypt that
        data = {"msgs": response.json()}
        response = mods.post('mixnet', entry_point=decrypt_url, baseurl=auth.url, json=data,
                response=True)

        if response.status_code != 200:
            # TODO: manage error
            pass

        self.tallyF = response.json()
        self.save()

        self.do_postproc()
    def votes_info_opciones(self):
        options = self.question.options.all()

        opts = []
        for opt in options:
            opts.append('option:'+ str(opt.option)) 
        return opts   

    def votes_info_votos(self):
        tally = self.tally
        options = self.question.options.all()

        opts = []
        for opt in options:
            if isinstance(tally, list):
                votes = tally.count(opt.number)
            else:
                votes = 0
            opts.append(
                str(votes)+" votes"
            )  
        
        return opts

    def do_postproc(self):
        tally = self.tally
        tallyM=self.tallyM
        tallyF=self.tallyF
        options = set()
        points = self.question.points
        for q in self.question.all():
            for o in q.options.all():
                options.add(o)

        opts = []
        for opt in options:
            votesM=tallyM.count(opt.number)
            votesF=tallyF.count(opt.number)
            if isinstance(tally, list) and len(tally) !=0 and isinstance(tally[0], list):
                m = [i for i,x in enumerate(tally[0]) if x==opt.number] 
                votes = [tally[1][j] for j in m]
                
            elif isinstance(tally, list) and len(tally) !=0:
                votes = tally.count(opt.number)         
            else:
                votes = 0
            opts.append({
                'option': opt.option,
                'number': opt.number,
                'votes': votes,
                'votes_masc': votesM,
                'votes_fem': votesF,
                'points': points
            })

        data = { 'type': self.type.name, 'options': opts }
        postp = mods.post('postproc', json=data)

        self.postproc = postp
        self.save()

    def __str__(self):
        return self.name
