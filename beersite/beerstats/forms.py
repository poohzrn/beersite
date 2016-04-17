from django import forms
from django.forms.widgets import SelectDateWidget
from django.utils import timezone
from beerstats.choices import INTERVALCHOICES


class OptionForm(forms.Form):
    interval = forms.ChoiceField(choices=INTERVALCHOICES,
            widget=forms.Select(attrs={"onChange": 'submit();'}))
    #start_date = forms.DateField(initial=timezone.now(),
    #        widget=SelectDateWidget(attrs={"onChange": 'submit();'}))
    #end_date = forms.DateField(initial=timezone.now(),
    #        widget=SelectDateWidget(attrs={"onChange": 'submit();'}))
