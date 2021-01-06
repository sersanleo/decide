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

        try:
            r = mods.get('voting', params={'id': vid})
            context['voting'] = json.dumps(r[0])
            if (r[0]['end_date'] != None):
                labels, data = self.get_identity_data(r[0])
                context['labels'] = labels
                context['data'] = data

        except:
            raise Http404

        return context

    def get_identity_data(self,voting):
        labels = []
        data = []
        postproc = voting.get('postproc')

        for voting in postproc[0]:
            labels.append(voting['option'])
            data.append(int(voting['postproc']))

        return labels,data

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

