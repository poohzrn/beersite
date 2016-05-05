"""
Views
"""
from django.shortcuts import render
from beerstats.forms import OptionForm
from beerstats.utils import get_chart_series


def index(request):
    "Default index view"
    template = 'beerstats/base.html'
    context = {'nav_active': 'home'}
    return render(request, template, context)


def graph(request, chart_id='chart_ID', chart_type='line', chart_height=500):
    """
    Graph/Chart view
    """
    template = 'beerstats/graph.html'
    if request.method == 'POST':
        options = OptionForm(data=request.POST)
        if options.is_valid():
            interval = int(options.cleaned_data['interval'])
            chart_type = options.cleaned_data['chart_type']
            series = get_chart_series(interval)

    else:
        options = OptionForm()
        series = get_chart_series()

    chart = {"renderTo": chart_id,
             "type": chart_type,
             "height": chart_height, }

    context = {'chartID': chart_id,
               'chart': chart,
               'series': series,
               'nav_active': 'graph',
               'options': options}
    return render(request, template, context)
