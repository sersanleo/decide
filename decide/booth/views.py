import json
import datetime
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.urls import reverse
from base import mods
from census.models import Census
from voting.models import Voting
from store.models import Vote
from django.contrib.auth.models import User
from .models import SuggestingForm

class LoginView(TemplateView):
    template_name = 'booth/login.html'

class LogoutView(TemplateView):
    template_name = 'booth/login.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        token = self.request.session.get('user_token')
        if token: 
            mods.post('authentication', entry_point='/logout/', json={'token':token})
            del self.request.session['user_token']
            del self.request.session['voter_id']
    
        return context

def autenticacion(request, username, password):
    token= mods.post('authentication', entry_point='/login/', json={'username':username, 'password':password})
    request.session['user_token']=token
    voter = mods.post('authentication', entry_point='/getuser/', json=token)
    voter_id = voter.get('id', None)
    request.session['voter_id'] = voter_id
    if voter_id == None:
        return False, voter_id
    return True, voter_id

def dashboard_details(voter_id):
    context={}
    vot_dis=[]
    context['no_censo'], context['no_vot_dis'] = False, False

    census_by_user = Census.objects.filter(voter_id=voter_id)
    if census_by_user.count() == 0 :
        context['no_censo'] = True
    else:
        for c in census_by_user:
            vid = c.voting_id
            try:
                votacion = Voting.objects.filter(end_date__isnull=True).exclude(start_date__isnull=True).get(id=vid)
                if Vote.objects.filter(voting_id=vid, voter_id=voter_id).count()==0:
                    vot_dis.append(votacion)
            except Exception:
                error= 'Esta votación ha sido borrada'

    context['vot_dis'] = vot_dis
    if len(vot_dis) == 0:
        context['no_vot_dis'] = True
    
    return context

def authentication_login(request):
    
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        # Autenticacion
        voter, voter_id = autenticacion(request, username, password)
        if not voter:
            return render(request, 'booth/login.html', {'no_user':True})
        else:
            context = dashboard_details(voter_id)
            return render(request, 'booth/dashboard.html', context)
    else:

        token = request.session.get('user_token', None)
        if token == None:
            return render(request, 'booth/login.html')
        else:
            voter_id = request.session.get('voter_id', None)
            context = dashboard_details(voter_id)
            return render(request, 'booth/dashboard.html', context)


class BoothView(TemplateView):
    template_name = 'booth/booth.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)
        token = self.request.session.get('user_token', None)
        context['token']= json.dumps(token.get('token', None))
        voter = mods.post('authentication', entry_point='/getuser/', json=token)
        context['voter']= json.dumps(voter)
        voter_id = voter.get('id', None)

        try:
            r = mods.get('voting', params={'id': vid})
            # Casting numbers to string to manage in javascript with BigInt
            # and avoid problems with js and big number conversion
            for k, v in r[0]['pub_key'].items():
                r[0]['pub_key'][k] = str(v)

            context['voting'] = json.dumps(r[0])
            context['votacion_id'] = vid
            context['multiple_option'] = int(json.dumps(r[0]['question']['option_types'])) == 2
            context['rank_order_scale'] = int(json.dumps(r[0]['question']['option_types'])) == 3

            if Vote.objects.filter(voting_id=vid, voter_id=voter_id).count()!=0:
                context['voted'] = True
        except:
            raise Http404 

        context['KEYBITS'] = settings.KEYBITS

        return context

class SuggestingFormView(TemplateView):
    template_name="booth/suggesting.html"

    def dispatch(self, request, *args, **kwargs):
        if not 'user_token' in request.session:
            return HttpResponseRedirect(reverse('login'))
        
        return super(SuggestingFormView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['post_data'] = check_unresolved_post_data(self.request.session)

        return context

class SuggestingDetailView(TemplateView):
    template_name="booth/suggesting.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sid = kwargs.get('suggesting_id', 0)
        user_id = self.request.session['voter_id']
        
        try:
            suggesting = SuggestingForm.objects.get(pk=sid)

            if suggesting.user_id == user_id:
                context['suggesting'] = suggesting
                
                if suggesting.is_approved:
                    context['suggesting_state'] = "Su sugerencia ha sido aprobada."
                elif suggesting.is_approved is None:
                    context['suggesting_state'] = "Su sugerencia está pendiente de revisión."
                else:
                    context['suggesting_state'] = "Su sugerencia ha sido rechazada."
            else:
                context['access_blocked'] = True
        except:
            raise Http404("Suggesting Form %s does not exist" % sid)

        return context

def send_suggesting_form(request):
    
    if request.method == 'POST':
        user_id = request.session['voter_id']
        title = request.POST['suggesting-title']
        str_s_date = request.POST['suggesting-date']
        content = request.POST['suggesting-content']
        send_date = timezone.now().date()

        s_date = datetime.datetime.strptime(str_s_date, '%Y-%m-%d').date()

        if is_future_date(s_date):
            s = SuggestingForm(user_id=user_id, title=title, suggesting_date=s_date, content=content, send_date=send_date)
            s.save()
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            request.session['title'] = title
            request.session['suggesting_date'] = str_s_date
            request.session['content'] = content
            request.session['errors'] = "La fecha seleccionada ya ha pasado. Debe seleccionar una posterior al día de hoy."
            return HttpResponseRedirect(reverse('suggesting-form'))
    else:
        return HttpResponseRedirect(reverse('dashboard'))

def is_future_date(date):
    return date > timezone.now().date()

def check_unresolved_post_data(session):
    context = {}

    if 'title' in session and 'suggesting_date' in session and 'content' in session and 'errors' in session:
        context['title'] = session['title']
        context['suggesting_date'] = session['suggesting_date']
        context['content'] = session['content']
        context['errors'] = session['errors']
        del session['title']
        del session['suggesting_date']
        del session['content']
        del session['errors']

    return context
