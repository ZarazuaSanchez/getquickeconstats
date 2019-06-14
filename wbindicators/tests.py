from django.test import TestCase
from wbindicators.models import IndicatorForm
from wbindicators.views import *

# Create your tests here.
country, indicator = 'MX', 'SP.POP.TOTL'
from_ = '1994'
to_ = ''

fillform = { 'my_country': country,
               'my_indicator': indicator,
               'from_': from_,
               'to_': to_ }

indicatorForm = IndicatorForm(fillform)
indicatorForm.is_valid()
wbdata = form_to_data(indicatorForm)
dictdata = parse_wbdata(wbdata, indicator, country)
