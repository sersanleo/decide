import json

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import Http404

from base import mods

from voting.models import Voting

from census.models import Census


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
            context['postproc'] = r[0]["postproc"][0]
            print(context)
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


def get_list_votings(request):
    filter = request.GET.get('filter')
    busqueda = request.GET.get('nombre')
    list = None
    try:
        if filter == 'F':
            list = Voting.objects.filter(start_date__isnull=False, end_date__isnull=False).all()
        elif filter == 'A':
            list = Voting.objects.filter(start_date__isnull=False, end_date__isnull=True).all()
        elif filter == 'S':
            list = Voting.objects.filter(start_date__isnull=True, end_date__isnull=True).all()
        else:
            if busqueda is None:
                list = Voting.objects.all()
            else:
                list = Voting.objects.filter(name__contains=busqueda).all()
    except:
        raise Http404
    #Si no soy superuser solo veo las votaciones en las que estoy censado
    if not request.user.is_superuser:
        census = Census.objects.filter(voter_id=request.user.id).all()
        new_list = []
        for c in census:
            for voting in list:
                if voting.id == c.voting_id:
                    new_list.append(voting)
        list = new_list
        user = False
    else:
        user = True
    return render(request, 'visualizer/listVisualizer.html', {'votings': list, 'user': user})

