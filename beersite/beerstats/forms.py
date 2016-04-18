from django import forms
from beerstats.choices import INTERVALCHOICES
from beerstats.choices import CHARTCHOICES


class OptionForm(forms.Form):
    interval = forms.ChoiceField(choices=INTERVALCHOICES,
            widget=forms.Select(attrs={"onChange": 'submit();'}))
    chart_type = forms.ChoiceField(choices=CHARTCHOICES,
            widget=forms.Select(attrs={"onChange": 'submit();'}))
