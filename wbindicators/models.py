from django.db import models
from django import forms

# Create your models here.

#make list of countries available at WB for select drop down menu
import wbpy
from datetime import date as d

api = wbpy.IndicatorAPI()
countries = api.get_countries()
country_choices = [ (code, countries[code]['name']) for code in countries]
country_choices.sort(key=lambda tup: tup[1])

indic_choices = [ ('EN.ATM.CO2.PP.GD.KD', 'CO2 Emissions'),
                  ('FP.CPI.TOTL.ZG', 'Inflation'),
                  ('SP.POP.TOTL', 'Population, total'),
                  ('SP.POP.GROW', 'Population, growth (annual %)'),
                  ('SH.HIV.INCD.ZS', 'Prevalence of HIV, total (% of population ages 15-49)')
                ]

#pophindicators = api.get_indicators(search="population", common_only=True, topic=8)
#indic_choices = [ (code, pophindicators[code]['name']) for code in pophindicators]

class IndicatorForm(forms.Form):
    my_country = forms.ChoiceField(choices=country_choices)
    my_indicator = forms.ChoiceField(choices=indic_choices)

    years = [( int(y), y ) for y in range( d.today().year - 1, 1959, -1 ) ]
    from_ = forms.ChoiceField(choices=years)
    years.insert(0, (None, 'Select a year'))
    to_ = forms.ChoiceField(choices=years, initial=(None, 'Select a year'), required=False)

    def is_valid(self):
        other_valid = forms.Form.is_valid(self)

        from_year = self.cleaned_data['from_']
        to_year = self.cleaned_data['to_']

        if to_year or from_year:
            return True and other_valid
        else:
            return False and other_valid

    def clean(self):
        cleaned_data = super().clean()
        from_year = cleaned_data.get("from_")
        to_year = cleaned_data.get("to_")

        if to_year:
            if int(from_year) > int(to_year):
                raise forms.ValidationError("Second year must be later than 1st year.")
