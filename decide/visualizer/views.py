import json

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import Http404

from base import mods
from voting.models import Voting
from census.models import Census
from store.models import Vote

class VisualizerView(TemplateView):
    template_name = 'visualizer/visualizer.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        try:
            # voting = Voting.objects.get(pk = vid)
            r = mods.get('voting', params={'id': vid})
            voting = r[0]
            # context['voting'] = json.dumps(voting)

            # Mostramos las gráficas de las votaciones finalizadas
            if not voting['end_date'] == None:
                postproc = voting ['postproc']
                # self.statistics_identity(r[0],context)
                # if voting.type == 'EQUALITY':
                # self.statistics_equality(context, voting)
                #elif voting.type == 'IDENTITY':

                # else:
                context = self.statistics_points(context, voting)

        except:
            raise Http404

        return context

    def statistics_equality(self, context, voting):
        
        postproc = [
            { 'option': 'Option 1', 'number': 1, 'votes_men': 2, 'votes_women': 3, 'postproc': 4 },
            { 'option': 'Option 3', 'number': 3, 'votes_men': 3, 'votes_women': 1, 'postproc': 4 },
            { 'option': 'Option 2', 'number': 2, 'votes_men': 0, 'votes_women': 4, 'postproc': 3 },
            { 'option': 'Option 5', 'number': 5, 'votes_men': 1, 'votes_women': 3, 'postproc': 3 },
            { 'option': 'Option 6', 'number': 6, 'votes_men': 1, 'votes_women': 1, 'postproc': 2 },
            { 'option': 'Option 4', 'number': 4, 'votes_men': 1, 'votes_women': 0, 'postproc': 1 }]

        options = []
        v_men = []
        v_women = []
        
        for opt in postproc:
            options.append(opt['option'])
            v_men.append(opt['votes_men'])
            v_women.append(opt['votes_women'])
        
        context['options'] = options
        context['v_men'] = v_men
        context['v_women'] = v_women


    def statistics_points(self, context, voting):
        # r = {}
        # r["name"] = "Nombre de la votación"
        # r["desc"] = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor " \
        #             "incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud "
        # r["type"] = 'IDENTITY'
        # r["options"] = [{'question': 'unique', 'question_id': 2, 'option': 'a', 'number': 4, 'votes': 7, 'votes_masc': 0,
        #                  'votes_fem': 4, 'points': 7, 'postproc': 3},
        #                 {'question': 'unique', 'question_id': 2, 'option': 'b', 'number': 5, 'votes': 6, 'votes_masc': 0,
        #                  'votes_fem': 5, 'points': 7, 'postproc': 2},
        #                 {'question': 'unique', 'question_id': 2, 'option': 'c', 'number': 6, 'votes': 4, 'votes_masc': 0,
        #                  'votes_fem': 1, 'points': 7, 'postproc': 1},
        #                 {'question': 'unique', 'question_id': 2, 'option': 'd', 'number': 7, 'votes': 9, 'votes_masc': 0,
        #                  'votes_fem': 1, 'points': 7, 'postproc': 1}]
        labels = []
        postproc = []
        votes = []
        points = voting['postproc'][0]['options'][0]['points']
        question = voting['postproc'][0]['options'][0]['question']
        type = voting['postproc'][0]["type"]
        name = voting["name"]
        desc = voting["desc"]
        for option in voting['postproc'][0]['options']:
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

    def statistics_identity(self,voting, context):
        labels = []
        data = []
        postproc = voting.get('postproc')

        for voting in postproc[0]:
            labels.append(voting['option'])
            data.append(int(voting['postproc']))
        context['labels'] = labels
        context['data'] = data

class VisualizerViewPointsInclude(TemplateView):
    template_name = 'visualizer/functionVisualizer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        try:
            # voting = Voting.objects.get(pk = vid)
            r = mods.get('voting', params={'id': vid})
            voting = r[0]
            # context['voting'] = json.dumps(voting)

            # Mostramos las gráficas de las votaciones finalizadas
            if not voting['end_date'] == None:
                postproc = voting ['postproc']
                # self.statistics_identity(r[0],context)
                # if voting.type == 'EQUALITY':
                # self.statistics_equality(context, voting)
                #elif voting.type == 'IDENTITY':

                # else:
                context = self.statistics_points(context, voting)

        except:
            raise Http404

        return context

    def statistics_points(self, context, voting):
        # r = {}
        # r["name"] = "Nombre de la votación"
        # r["desc"] = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor " \
        #             "incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud "
        # r["type"] = 'IDENTITY'
        # r["options"] = [{'question': 'unique', 'question_id': 2, 'option': 'a', 'number': 4, 'votes': 7, 'votes_masc': 0,
        #                  'votes_fem': 4, 'points': 7, 'postproc': 3},
        #                 {'question': 'unique', 'question_id': 2, 'option': 'b', 'number': 5, 'votes': 6, 'votes_masc': 0,
        #                  'votes_fem': 5, 'points': 7, 'postproc': 2},
        #                 {'question': 'unique', 'question_id': 2, 'option': 'c', 'number': 6, 'votes': 4, 'votes_masc': 0,
        #                  'votes_fem': 1, 'points': 7, 'postproc': 1},
        #                 {'question': 'unique', 'question_id': 2, 'option': 'd', 'number': 7, 'votes': 9, 'votes_masc': 0,
        #                  'votes_fem': 1, 'points': 7, 'postproc': 1}]
        labels = []
        postproc = []
        votes = []
        points = voting['postproc'][0]['options'][0]['points']
        question = voting['postproc'][0]['options'][0]['question']
        type = voting['postproc'][0]["type"]
        name = voting["name"]
        desc = voting["desc"]
        for option in voting['postproc'][0]['options']:
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

def get_global_view(request):

    vt = 0
    ct = 0
    nvs = 0

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