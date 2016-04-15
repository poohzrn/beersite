from django import forms
from beerstats.models import Brew
from beerstats.choices import INTERVALCHOICES
from beerstats.choices import CHARTCHOICES


class OptionForm(forms.Form):
    brew = forms.ModelChoiceField(
            queryset=Brew.objects.all(),
            widget=forms.Select(attrs={"onChange": 'submit();'}))
    interval = forms.ChoiceField(
                choices=INTERVALCHOICES,
                widget=forms.Select(attrs={"onChange": 'submit();'}))
    chart_type = forms.ChoiceField(
                 choices=CHARTCHOICES,
                 widget=forms.Select(attrs={"onChange": 'submit();'}))
