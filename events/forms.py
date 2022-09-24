from django import forms
from django.forms import ModelForm
from . models import Venue, Event

#Create a Venue Form
class VenueForm(ModelForm):
	class Meta:
		model = Venue
		fields = ('name', 'address', 'Zip_code', 'phone', 'web', 'email_address', 'venue_image')

		labels = {
			'name': '',
			'address': '',
			'Zip_code': '',
			'phone': '',
			'web': '',
			'email_address': '',
			'venue_image': '',

		}

		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Venue Name'}),
			'address': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address'}),
			'Zip_code': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zip Code'}),
			'phone': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone'}),
			'web': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Website'}),
			'email_address': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}),
		}
#Admine SuperUser Event Form
class EventFormAdmin(ModelForm):
	class Meta:
		model = Event
		fields = ('name', 'event_date', 'venue', 'manager', 'description', 'attendess')

		labels = {
			'name': '',
			'event_date': 'YYYY: MM: DD:',
			'venue' : 'Venue',
			'manager' : 'Manager',
			'description': '',
			'attendess' : 'Attendees',

		}

		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Event Name'}),
			'event_date': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Event Date'}),
			'venue': forms.Select(attrs={'class':'form-control', 'placeholder':'Venue'}),
			'manager': forms.Select(attrs={'class':'form-control', 'placeholder':'Manager'}),
			'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Description'}),
			'attendess': forms.SelectMultiple(attrs={'class':'form-control', 'placeholder':'Attendes'}),
		}

#User Event Form
class EventForm(ModelForm):
	class Meta:
		model = Event
		fields = ('name', 'event_date', 'venue', 'description', 'attendess')

		labels = {
			'name': '',
			'event_date': 'YYYY: MM: DD:',
			'venue' : 'Venue',
			'description': '',
			'attendess' : 'Attendees',

		}

		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Event Name'}),
			'event_date': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Event Date'}),
			'venue': forms.Select(attrs={'class':'form-control', 'placeholder':'Venue'}),			'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Description'}),
			'attendess': forms.SelectMultiple(attrs={'class':'form-control', 'placeholder':'Attendes'}),
		}
