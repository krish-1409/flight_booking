from django.contrib.auth.models import User
from django import forms

sort_by = [
    ('score','SCORE'),
    ('price','PRICE'),
    ('duration','DURATION'),

]


class FlightSearchForm(forms.Form):
    source = forms.CharField(label='source', max_length=20)
    destination = forms.CharField(label='destination', max_length=20)
    date = forms.DateField()
    sort_by = forms.CharField(label='choose your preference.',widget=forms.Select(choices=sort_by))

    class Meta():
        model = User
        fields = ['source','destination','date','sort_by']





