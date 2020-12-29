import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from base import mods
from voting.models import Voting


# TODO: check permissions and census
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
            context['votacion_id'] = vid

        except:
            raise Http404

        context['KEYBITS'] = settings.KEYBITS

        return context

def style_change(request):
    if request.method == 'POST': 
        vid = request.POST['votacion'] 

        try:
            r = mods.get('voting', params={'id': vid})

            # Casting numbers to string to manage in javascript with BigInt
            # and avoid problems with js and big number conversion
            for k, v in r[0]['pub_key'].items():
                r[0]['pub_key'][k] = str(v)

            return render(request, 'booth/booth.html', {'d_p':True, 'KEYBITS':settings.KEYBITS, 'voting':json.dumps(r[0])})

        except:
            raise Http404

        return render(request, 'booth/booth.html', {'d_p':False, 'KEYBITS':settings.KEYBITS})

    else:
        return render(request, 'booth/booth.html', {'error':"Debes pasar primero por login"})