from django.shortcuts import render
from beerstats.forms import OptionForm
from beerstats.utils import ChartData


def index(request):
    template = 'beerstats/base.html'
    context = {'nav_active': 'home'}
    return render(request, template, context)


def graph(request, chartID='chart_ID', chart_type='line', chart_height=500):
    template = 'beerstats/graph.html'
    if request.method == 'POST':
        options = OptionForm(data=request.POST)
        if options.is_valid():
            interval = int(options.cleaned_data['interval'])
            chart_type = options.cleaned_data['chart_type']
            data = ChartData.get_data(interval)

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

    chart = {"renderTo": chartID,
             "type": chart_type,
             "height": chart_height, }

    context = {'chartID': chartID,
               'chart': chart,
               'series': series,
               'options': options}
    return render(request, template, context)
