from django import forms
import datetime
from django.forms.extras.widgets import SelectDateWidget
from django.forms import ModelForm, Form


ATTRACTIONS_OPTIONS = ['Architecture','Art & Culture','History','Kids/Family',
					   'Landmarks & Sightseeing','Museums','Parks & Nature',
					   'Sports & Entertainment']
TRANS_OPTIONS = ['Drive', 'Public']

def _dropdown_menu(options):
	return [(x,x) for x in options]

ATTRACTIONS = _dropdown_menu(ATTRACTIONS_OPTIONS)
TRANS = _dropdown_menu(TRANS_OPTIONS)

class RecommendationForm(forms.Form):
	checkin = forms.DateField(
		    widget=SelectDateWidget,
		    label='Check-in Date',
		    required=False)
	checkout = forms.DateField(
		    widget=SelectDateWidget,
		    label='Check-out Date',
		    required=False)
	pricemin = forms.IntegerField(
			label='Minimum Price',
			help_text='e.g. 50',
			required=False)
	pricemax = forms.IntegerField(
			label='Maximum Price',
			help_text='e.g. 100',
			required=False)
	attraction = forms.MultipleChoiceField(
		    label='Attractions Preferences',
		    choices=ATTRACTIONS,
		    widget=forms.CheckboxSelectMultiple,
		    required=False)
	trans = forms.ChoiceField(
		    label='Transportation Type Preference',
		    choices=TRANS,
		    required=True)

	
	









