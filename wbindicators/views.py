from django.shortcuts import render
from django.template import loader
from django.urls import reverse
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

from django.http import HttpResponseRedirect
from .models import IndicatorForm

import wbdata, wbpy

api = wbpy.IndicatorAPI()

from datetime import datetime
from collections import OrderedDict, namedtuple

IndicInfo = namedtuple('IndicInfo', 'country indicname')

def home(request):
    form = IndicatorForm()
    temp = loader.get_template('requestindic.html')
    return HttpResponse(temp.render({'form': form}, request))

    #return HttpResponseRedirect(reverse('wbindicators:view_results', kwargs={'wbdata': data.as_dict()['MX'], } ))

#reverse cannot find view_results with Indicator
def view_results(request):

    myform = IndicatorForm(request.POST)

    if myform.is_valid():
        country = myform.cleaned_data['my_country'] #request.POST['my_country']
        indicator = myform.cleaned_data['my_indicator']#request.POST['my_indicator']
        fromyr = myform.cleaned_data['from_year'] #request.POST['from_']
        toyr = myform.cleaned_data['to_year'] #request.POST['to']

    #country = ['MX'] request.POST['my_country'
    #indicator = 'EN.ATM.CO2E.KT' #request.POST['my_indicator']
    #year = '2001' #request.POST['year']

        if toyr:
            data = (wbdata.get_data(indicator,
                    [country],
                    data_date=( datetime(int(fromyr), 1, 1), datetime(int(toyr), 1, 1))))
        else:
            data = (wbdata.get_data(indicator,
                    [country],
                    data_date=( datetime(int(fromyr), 1, 1))))
        
        wbindics = api.get_indicators(search=indicator)
        indicname = wbindics[indicator]['name']

        indinfo = IndicInfo(country, indicname)

        dictdata = {indinfo: {}}

        #collect dict of years and corresponding data
        for x in data:
            dictdata[indinfo][x['date']] = x['value']

        return render(request, 'results.html', {'data': dictdata } )

"""def home(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = IndicatorForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            if form.is_bound():

            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:

                return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = IndicatorForm()

    return render(request, 'requestindic.html', {'form': form})"""
    #return render(request, 'results.html', {'data': form})
