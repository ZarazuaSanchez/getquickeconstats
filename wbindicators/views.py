from django.shortcuts import render
from django.template import loader
from django.urls import reverse, reverse_lazy
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

from django.http import HttpResponseRedirect
from .models import IndicatorForm

from . import views

import wbdata, wbpy
api = wbpy.IndicatorAPI()

def form_to_data(myform):
    country = myform.cleaned_data['my_country']
    indicator = myform.cleaned_data['my_indicator']
    fromyr = int(myform.cleaned_data['from_'])
    toyr = myform.cleaned_data['to_']

    try:
        if toyr:
            toyr = int(toyr)
            data = wbdata.get_data( indicator,
                                    [country],
                                    data_date=(datetime(fromyr, 1, 1), datetime(toyr, 1, 1)))
        else:
            data = wbdata.get_data( indicator,
                                    [country],
                                    data_date=datetime(fromyr, 1, 1))
        return data

    except IndexError('No data'):
        return render(request, 'request_stats.html', {'form': myform})

from datetime import datetime
from collections import OrderedDict, namedtuple
IndicInfo = namedtuple('IndicInfo', 'country readable')

def parse_wbdata(wbdata, indicator, country):
    wbindics = api.get_indicators(search=indicator)
    readable = wbindics[indicator]['name']

    indicinfo = IndicInfo(country, readable)

    dictdata = {indicinfo: {}}

    for x in wbdata:
        dictdata[indicinfo][x['date']] = x['value']

    return dictdata

def request_stats(request):
    form = IndicatorForm()
    temp = loader.get_template('request_stats.html')
    return HttpResponse(temp.render({'form': form}, request))

def view_results(request):

    if request.method == 'POST':
        myform = IndicatorForm(request.POST)

        if myform.is_valid():
            wbdata = form_to_data(myform)
            dictdata = parse_wbdata(
                                    wbdata,
                                    myform.cleaned_data['my_indicator'],
                                    myform.cleaned_data['my_country']
            )

            return render(request, 'results.html', {'data': dictdata})
        #return HttpResponseRedirect(reverse('wbindicators:view_results', kwargs={'request': request, 'dictdata':dictdata}))
        #, kwargs={'dictdatva': dictdata, }))

    else:
        myform = IndicatorForm()

    return render(request, 'request_stats.html', {'form': myform})
