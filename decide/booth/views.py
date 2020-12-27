import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from store.models import Vote
from django.shortcuts import get_object_or_404

from base import mods


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

def check_census(request):
    vid = request.data.get('voting')
    uid = request.data.get('voter')

    # comprobamos que existan esos parametros
    if not vid or not uid:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    # validando votante
    token = request.auth.key
    voter = mods.post('authentication', entry_point='/getuser/', json={'token': token})
    voter_id = voter.get('id', None)
    if not voter_id or voter_id != uid:
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)

    # el usuario esta en el censo
    perms = mods.get('census/{}'.format(vid), params={'voter_id': uid}, response=True)
    if perms.status_code == 401:
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)

    # el usuario ha votado
    vote = get_object_or_404(Vote, voting_id=vid, voter_id=uid)
