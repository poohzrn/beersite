from django.shortcuts import render
from datetime import timedelta
from django.utils import timezone
from beerstats.forms import OptionForm
from beerstats.utils import ChartData


def index(request):
    template = 'beerstats/base.html'
    context = {'nav_active': 'home'}
    return render(request, template, context)


def graph(request, chartID='chart_ID', chart_type='line', chart_height=500):
    template = 'beerstats/graph.html'
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, }
    if request.method == 'POST':
        options = OptionForm(data=request.POST)
        if options.is_valid():
            interval = int(options.cleaned_data['interval'])
            # This suck
            # date_from = options.cleaned_data['start_date']
            # date_to = options.cleaned_data['end_date']
            date_from = timezone.now() - timedelta(days=7)
            date_to = timezone.now()
            data = ChartData.get_data(date_from, date_to, interval)

    else:
        options = OptionForm()
        data = ChartData.get_data()

    # Map the data to series
    series = []
    for dataitem in data:
        itemdata = []
        for interval, count in sorted(data[dataitem].items()):
            itemdata.append([str(interval), count])
        series.append({"name": dataitem, "data": itemdata})

    context = {'chartID': chartID,
               'chart': chart,
               'series': series,
               'options': options}
    return render(request, template, context)
