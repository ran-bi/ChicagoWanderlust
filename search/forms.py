# Code substantially modified, made reading the documentation at 
# https://docs.djangoproject.com/en/1.10/ref/forms/

from django import forms
import datetime
from django.forms.extras.widgets import SelectDateWidget
from django.forms import ModelForm, Form


ATTRACTIONS_OPTIONS = ['None', 'Architecture','Art & Culture','History','Kids/Family',
					   'Landmarks & Sightseeing','Museums','Parks & Nature',
					   'Sports & Entertainment']
TRANS_OPTIONS = ['driving','transit']

def _dropdown_menu(options):
	return [(x,x) for x in options]

ATTRACTIONS = _dropdown_menu(ATTRACTIONS_OPTIONS)
TRANS = _dropdown_menu(TRANS_OPTIONS)

class RecommendationForm(forms.Form):
	checkin = forms.DateField(
		    widget=SelectDateWidget,
		    label='Check-in(*)',
		    required=False)
	checkout = forms.DateField(
		    widget=SelectDateWidget,
		    label='Check-out(*)',
		    required=False)
	pricemin = forms.IntegerField(
			label='Min Price(*)',
			help_text='e.g. 100',
			required=False)
	pricemax = forms.IntegerField(
			label='Max Price(*)',
			help_text='e.g. 500',
			required=False)
	attraction_1 = forms.ChoiceField(
		    label='Attraction 1st Preference',
		    choices=ATTRACTIONS,
		    required=False)
	attraction_2 = forms.ChoiceField(
		    label='Attraction 2nd Preference',
		    choices=ATTRACTIONS,
		    required=False)
	attraction_3 = forms.ChoiceField(
		    label='Attraction 3rd Preference',
		    choices=ATTRACTIONS,
		    required=False)
	trans = forms.ChoiceField(
		    label='Transportation',
		    choices=TRANS,
		    required=True)

	
	









