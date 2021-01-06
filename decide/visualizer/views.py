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
            voting = Voting.objects.get(pk = vid)
            r = mods.get('voting', params={'id': vid})
            context['voting'] = json.dumps(r[0])

            # Mostramos las gráficas de las votaciones finalizadas
            if not voting.end_date == None:

                #if voting.type == 'EQUALITY':
                    self.statistics_equality(context, voting)
                #elif voting.type == 'IDENTITY':

                #else:

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


