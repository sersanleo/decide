import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404

from base import mods


class VisualizerView(TemplateView):
    template_name = 'visualizer/visualizer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)
        labels = []
        data = []

        try:
            r = mods.get('voting', params={'id': vid})
            context['voting'] = json.dumps(r[0])
        except:
            raise Http404

        #postproc = r[0].get('postproc')
        postproc = [
            {'option': 'Option E', 'number': 5, 'points': 21, 'votes': 391000, 'postproc': 8},
            {'option': 'Option F', 'number': 6, 'points': 21, 'votes': 311000, 'postproc': 7},
            {'option': 'Option B', 'number': 2, 'points': 21, 'votes': 184000, 'postproc': 4},
            {'option': 'Option C', 'number': 3, 'points': 21, 'votes': 73000, 'postproc': 2},
            {'option': 'Option G', 'number': 7, 'points': 21, 'votes': 27000, 'postproc': 0},
            {'option': 'Option A', 'number': 1, 'points': 21, 'votes': 12000, 'postproc': 0},
            {'option': 'Option D', 'number': 4, 'points': 21, 'votes': 2000, 'postproc': 0},
        ]

        for voting in postproc :
            labels.append(voting['option'])
            data.append(int(voting['postproc']))

        context['labels'] = labels
        context['data'] = data

        return context
