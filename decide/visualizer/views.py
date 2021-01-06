import json

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import Http404

from base import mods
from census.models import Census
from store.models import Vote

from voting.models import Voting



class VisualizerView(TemplateView):
    template_name = 'visualizer/visualizer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        try:
            r = mods.get('voting', params={'id': vid})
            context['voting'] = json.dumps(r[0])
            context['postproc'] = r[0]["postproc"][0]
            print(context)
        except:
            raise Http404

        return context

class VisualizerViewPointsInclude(TemplateView):
    template_name = 'visualizer/functionVisualizer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)
        voting = mods.get('voting', params={'id': vid})

        context = self.statistics_points(voting, context)

        return context

    def statistics_points(self, voting, context):
        r={}
        r["name"] = "Nombre de la votación"
        r["desc"] = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor " \
                    "incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud "
        r["type"] = 'IDENTITY'
        r["options"] = [{'question':'unique', 'question_id': 2, 'option': 'a', 'number':4, 'votes': 7, 'votes_masc':0, 'votes_fem': 4, 'points': 7, 'postproc': 3},
                        {'question':'unique', 'question_id': 2, 'option': 'b', 'number':5, 'votes': 6, 'votes_masc':0, 'votes_fem': 5, 'points': 7, 'postproc':2},
                        {'question':'unique', 'question_id': 2, 'option': 'c', 'number':6, 'votes': 4, 'votes_masc':0, 'votes_fem': 1, 'points': 7, 'postproc': 1},
                        {'question':'unique', 'question_id': 2, 'option': 'd', 'number': 7, 'votes': 9, 'votes_masc':0, 'votes_fem': 1, 'points': 7, 'postproc': 1}]
        voting = r
        labels = []
        postproc = []
        votes = []
        points =  voting['options'][0]['points']
        question = voting['options'][0]['question']
        type = voting['type']
        name = voting["name"]
        desc = voting["desc"]
        for option in voting['options']:
            labels.append(option['option'])
            postproc.append((option['postproc']))
            votes.append(option['votes'])

        context['labels'] = labels
        context['postproc'] = postproc
        context['votes'] = votes
        context['question'] = question
        context['points'] = points
        context['type'] = type
        context['name'] = name
        context['desc'] = desc

        return context


class StatisticsView(TemplateView):
    template_name = 'visualizer/statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        try:
            r = mods.get('voting', params={'id': vid})
            census = Census.objects.filter(voting_id=vid).all()
            votes = Vote.objects.filter(voting_id=vid).all()
            c=census.count()
            v=votes.count()
            stat = {"census":c}
            stat["votes"] = v
            if v>0:
                stat["percentage"] = round(v/c*100,2);
            else:
                stat["percentage"] = 0;
            context['voting'] = json.dumps(r[0])
            context['stats'] = json.dumps(stat)
        except:
            raise Http404

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
