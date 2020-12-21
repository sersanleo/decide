from django import forms
from django.contrib import admin
from django.utils import timezone
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from django.contrib import messages

from .models import QuestionOption
from .models import Question
from .models import Voting
from census.models import Census

from .filters import StartedFilter

def start(modeladmin, request, queryset):
    for v in queryset.all():
        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()


def stop(ModelAdmin, request, queryset):
    for v in queryset.all():
        v.end_date = timezone.now()
        v.save()

def tally(ModelAdmin, request, queryset):
    for v in queryset.filter(end_date__lt=timezone.now()):
        token = request.session.get('auth-token', '')
        v.tally_votes(token)
        respuesta=give_message(v)
        messages.info(request,respuesta)

def give_message(v):
    mensj=""
    for i,j in zip(v.votes_info_opciones(),v.votes_info_votos()):
        if(i==v.votes_info_opciones()[-1] and j==v.votes_info_votos()[-1]):
            mensj=mensj+" in "+i+" it has got "+j+"."
        else:
            mensj=mensj+" in "+i+" it has got "+j+"," 

    respuesta="For voting:"+str(v.get_info().name)+mensj
    return respuesta


class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption


class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionOptionInline]

class VotingModel(forms.ModelForm):
    autocenso = forms.BooleanField(required=False)

    class Meta:
        model = Voting
        exclude = []


class VotingAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    readonly_fields = ('start_date', 'end_date', 'pub_key',
                       'tally', 'postproc')
    # date_hierarchy = 'start_date'
    # list_filter = (StartedFilter,)
    list_filter = (StartedFilter, ('start_date', DateRangeFilter), ('end_date', DateRangeFilter),)
    search_fields = ('name', )

    actions = [ start, stop, tally ]
    form =VotingModel

    def save_model(self, request, obj, form, change):
        super(VotingAdmin, self).save_model(request, obj, form, change)
        if form.cleaned_data.get('autocenso'):
            user = request.user
            Census.objects.get_or_create(voter_id=user.id, voting_id=obj.id)



admin.site.register(Voting, VotingAdmin)
admin.site.register(Question, QuestionAdmin)
