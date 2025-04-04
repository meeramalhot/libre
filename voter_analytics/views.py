from django.shortcuts import render

# Create your views here.
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . models import *
import plotly
import plotly.graph_objs as go
from datetime import datetime


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
    '''View to display single voter'''

    model = Voter
    template_name = 'voter_analytics/voter.html'
    context_object_name = 'voter'


class VoterGraphView(ListView):
    '''View to show graphs of voter data.'''

    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = 'voter'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voter = context['voter']

        total_voters = self.get_queryset()

        voter_dob = {}
        for voter in total_voters:
            year = voter.dob.year
            #add to key w .get
            voter_dob[year] = voter_dob.get(year, 0) + 1

        sorted_years = sorted(voter_dob.keys())
        x = sorted_years
        y = [voter_dob[year] for year in sorted_years]

        fig = go.Bar(x=x, y=y)
        title_text = "Voter Date of Birth Distribution"
        dob_bar = plotly.offline.plot(
             {"data": [fig], "layout": {"title": title_text}},
             auto_open=False,
             output_type="div"
        )

        context['dob_bar'] = dob_bar


        #PIE CHART
        # dict for party: count
        party_totals = {}

        for voter in total_voters:
            party = voter.party_affiliation
            if party:
                 if party in party_totals:
                    party_totals[party] += 1
                 else:
                    party_totals[party] = 1
        
        x = list(party_totals.keys()) 
        y = list(party_totals.values()) 

        fig = go.Pie(labels=x, values=y) 

        title_text = f"Voters by their party affiliation"
        # obtain the graph as an HTML div"
        party_pie = plotly.offline.plot({"data": [fig], 
                                         "layout_title_text": title_text,
                                         }, 
                                         auto_open=False, 
                                         output_type="div")
        
        # send div as template context variable
        context['party_pie'] = party_pie

        #BAR CHART 2

        election_counts = {
            'v20state': 0,
            'v21town': 0,
            'v21primary': 0,
            'v22general': 0,
            'v23town': 0,
        }

        for voter in total_voters:
            if voter.v20state == True:
                election_counts['v20state'] += 1
            if voter.v21town == True:
                election_counts['v21town'] += 1
            if voter.v21primary == True:
                election_counts['v21primary'] += 1
            if voter.v22general == True:
                election_counts['v22general'] += 1
            if voter.v23town == True:
                election_counts['v23town'] += 1

        x = list(election_counts.keys())
        y = list(election_counts.values())

        fig = go.Bar(x=x, y=y)
        title_text = "Votes per Election"
        elect_bar = plotly.offline.plot(
            {"data": [fig], "layout": {"title": title_text}},
            auto_open=False,
            output_type="div"
        )

        context['elect_bar'] = elect_bar

        return context  
