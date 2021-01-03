import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from django.core import serializers

from census.models import Census
from voting.models import Voting
from voting.serializers import MinimalVotingSerializer
from store.models import Vote

from base import mods

# TODO: check permissions and census
class IndexView(TemplateView):
    template_name = 'decide/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_id = self.request.user.id
        my_votings = Census.objects.filter(voter_id=user_id).values_list('voting_id', flat=True).distinct()
        pending_votings = []
        past_votings = []
        for vid in my_votings:
            try:
                voting = Voting.objects.get(id=vid)
                votes = Vote.objects.filter(voter_id=user_id, voting_id=vid).count()
                print(voting.tally)
                if votes == 0 and voting.start_date != None and voting.end_date == None:
                    pending_votings.append(voting)
                elif votes > 0 and voting.start_date != None and voting.end_date != None and voting.tally != None:
                    past_votings.append(voting)
            except:
                pass

        context['pending_votings'] = json.dumps(MinimalVotingSerializer(pending_votings, many=True).data)
        context['past_votings'] = json.dumps(MinimalVotingSerializer(past_votings, many=True).data)
        return context