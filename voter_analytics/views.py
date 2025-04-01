from django.shortcuts import render

# Create your views here.
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . models import *
import plotly
import plotly.graph_objs as go

class VotersListView(ListView):
    '''View to display marathon results'''

    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voter'
    paginate_by = 100