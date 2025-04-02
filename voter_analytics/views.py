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

    def get_queryset(self):
      results = super().get_queryset().order_by('last_name')

      if 'party_affiliation' in self.request.GET:
          party = self.request.GET['party_affiliation']
          if party:
              results = results.filter(party_affiliation=party)
      
      if 'min_dob' in self.request.GET:
          min_year = self.request.GET['min_dob']
          if min_year:
              results = results.filter(dob__year__gte=min_year)
      
      if 'max_dob' in self.request.GET:
          max_year = self.request.GET['max_dob']
          if max_year:
              results = results.filter(dob__year__lte=max_year)
      
      if 'voter_score' in self.request.GET:
          score = self.request.GET['voter_score']
          if score:
              results = results.filter(voter_score=score)
      
      if 'v20state' in self.request.GET:
          results = results.filter(v20state=True)
      if 'v21town' in self.request.GET:
          results = results.filter(v21town=True)
      if 'v21primary' in self.request.GET:
          results = results.filter(v21primary=True)
      if 'v22general' in self.request.GET:
          results = results.filter(v22general=True)
      if 'v23town' in self.request.GET:
          results = results.filter(v23town=True)
      
      return results


class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter.html'
    context_object_name = 'voter'