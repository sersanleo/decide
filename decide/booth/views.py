import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from base import mods
from census.models import Census
from voting.models import Voting
from store.models import Vote
from django.contrib.auth.models import User

class LoginView(TemplateView):
    template_name = 'booth/login.html'

class DashboardView(TemplateView):
    template_name = 'booth/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = kwargs.get('user_id', 0)
        context['user_id'] = user_id

        vot_dis = []
        no_censo, no_vot_dis = False, False

        census_by_user = Census.objects.filter(voter_id=user_id)
        if census_by_user.count() == 0 :
            context['no_censo'] = True
        else:
            for c in census_by_user:
                vid = c.voting_id
                try:
                    votacion = Voting.objects.filter(end_date__isnull=True).exclude(start_date__isnull=True).get(id=vid)
                    if Vote.objects.filter(voting_id=vid, voter_id=user_id).count()==0:
                        vot_dis.append(votacion)
                except Exception:
                    error= 'Esta votación ha sido borrada'
        context['vot_dis'] = vot_dis

        if len(vot_dis) == 0:
            context['no_vot_dis'] = True

        return context

class BoothView(TemplateView):
    template_name = 'booth/booth.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)
        user_id = kwargs.get('user_id', 0)
        
        try:
            r = mods.get('voting', params={'id': vid})

            # Casting numbers to string to manage in javascript with BigInt
            # and avoid problems with js and big number conversion
            for k, v in r[0]['pub_key'].items():
                r[0]['pub_key'][k] = str(v)

            context['voting'] = json.dumps(r[0])

            if Vote.objects.filter(voting_id=vid, voter_id=user_id).count()!=0:
                context['voted'] = True 
        except:
            raise Http404 

        context['KEYBITS'] = settings.KEYBITS

        return context
