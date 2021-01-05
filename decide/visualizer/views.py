import json
from django.views.generic import TemplateView
from django.shortcuts import render
from django.conf import settings
from django.http import Http404
from census.models import Census
from store.models import Vote
from voting.models import Voting
from base import mods
from census.models import Census
from store.models import Vote



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
        votings = Voting.objects.all()
        abstm = 0
        porvotm = 0
        vtm = 0
        ctm = 0
        abstr = 999999999999999999
        porvotr = 999999999999999999
        vtr = 999999999999999999
        ctr = 999999999999999999
        tabst = 0
        tporvot = 0
        for vot in votings:
            if vot.end_date:
                vid = vot.id
                census = Census.objects.filter(voting_id=vid).all().count()
                votes = Vote.objects.filter(voting_id=vid).all().count()
                #Votos totales y mayor / menor
                vt = vt + votes
                if vtm < votes:
                    vtm = votes
                if vtr > votes:
                    vtr = votes
                #Censo total y mayor / menor
                ct = ct + census
                if ctm < census:
                    ctm = census 
                if ctr > census:
                    ctr = census

                #Numero de votaciones
                nvs = nvs + 1
                #Porcentaje de abstencion y mayor / menor
                if census != 0:
                    abst = ((votes/census)-1)*(-100)
                    tabst = tabst + abst
                    if abstm < abst:
                        abstm = abst
                    if abstr > abst:
                        abstr = abst
                #Porcentaje de voto y mayor / menor
                    porvot = (votes/census)*100
                    tporvot = tporvot + porvot
                    if porvotm < porvot:
                        porvotm = porvot
                    if porvotr > porvot:
                        porvotr = porvot
                        
    except:
            
        raise Http404
        
    return render(request, 'visualizer/globalVisualizer.html', {'votes': vt, 'votesm': vtm, 'census': ct, 'censusm': ctm, 'nvoting': nvs, 
    'abst': tabst, 'abstm': abstm, 'porvot': tporvot, 'porvotm': porvotm, 'porvotr': porvotr, 'abstr': abstr, 'votesr': vtr, 'censusr': ctr})