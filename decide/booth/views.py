import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from base import mods
from census.models import Census
from voting.models import Voting

class LoginView(TemplateView):
    template_name = 'booth/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['KEYBITS'] = settings.KEYBITS

        return context

def dashboardView(request):
    if request.method == 'POST':
        user_id = request.POST['user']
        try:
            census_by_user = Census.objects.filter(voter_id=user_id)
            votaciones = []
            for c in census_by_user:
                vid = c.voting_id
                try:
                    votacion = Voting.objects.filter(end_date__isnull=True).exclude(start_date__isnull=True).get(id=vid)
                    votaciones.append(votacion)
                except Exception:
                    error= 'Esta votación ha sido borrada'
                    
        except Exception:
            error = 'No existen votaciones para este usuario'
        
        return render(request, 'booth/dashboard.html', {'signup':False, 'votaciones':votaciones})
    else:
        return render(request, 'booth/login.html', {'KEYBITS': settings.KEYBITS})

class BoothView(TemplateView):
    template_name = 'booth/booth.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        try:
            r = mods.get('voting', params={'id': vid})

            # Casting numbers to string to manage in javascript with BigInt
            # and avoid problems with js and big number conversion
            for k, v in r[0]['pub_key'].items():
                r[0]['pub_key'][k] = str(v)

            context['voting'] = json.dumps(r[0])
        except:
            raise Http404

        context['KEYBITS'] = settings.KEYBITS

        return context
