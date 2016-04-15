from django.shortcuts import render
from beerstats.models import Brew
from beerstats.utils import get_intervals
from beerstats.utils import get_chart_data
from beerstats.forms import OptionForm

from graphos.sources.simple import SimpleDataSource
from graphos.renderers import gchart
from django.utils import timezone


def index(request):
    template = 'beerstats/base.html'
    context = {'nav_active': 'home'}
    return render(request, template, context)


def graph(request):
    template = 'beerstats/graph.html'
    time_from = timezone.now()
    chart = None
    chart_type = 'line'
    options = OptionForm()

    if request.method == 'POST':

        options = OptionForm(data=request.POST)

        if options.is_valid():

            interval = int(options.cleaned_data['interval'])
            brew_id = options.cleaned_data['brew'].id
            chart_type = options.cleaned_data['chart_type']
            brew = Brew.objects.get(id=brew_id)
            time_from = brew.start_time
            intervals = get_intervals(interval, time_from, timezone.now())
            data = get_chart_data(intervals, interval, brew.id)
            chart = gchart.ColumnChart(SimpleDataSource(data=data))

    context = {'chart': chart,
               'chart_type': chart_type,
               'options': options,
               'nav_active': 'graph'}

    return render(request, template, context)
