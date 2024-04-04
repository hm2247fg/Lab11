from django import forms  # Importing necessary modules from Django
from django.forms import FileInput, DateInput  # Importing specific form field types
from .models import Place  # Importing the Place model from the current directory


# Defining a form for adding a new place
class NewPlaceForm(forms.ModelForm):
    class Meta:  # Meta class to specify metadata for the form
        model = Place  # Specify the model for which the form is created
        fields = ('name', 'visited')  # Specify the fields to include in the form


# Define a custom date input field to ensure a date picker is displayed.
class DateInput(forms.DateInput):  # Defining a custom DateInput field
    input_type = 'date'  # Override the default input type to 'date'


class TripReviewForm(forms.ModelForm):  # Defining a form for reviewing a trip
    class Meta:  # Metaclass to specify metadata for the form
        model = Place  # Specify the model for which the form is created
        fields = ('notes', 'date_visited', 'photo')  # Specify the fields to include in the form
        widgets = {  # Define custom widgets for form fields
            'date_visited': DateInput()  # Apply DateInput widget to the date_visited field
        }
