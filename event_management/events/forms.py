from django import forms
from .models import Event, Participant, Task
from django import forms

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'time', 'location']

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['description', 'completed']


class EmailForm(forms.Form):
    email = forms.EmailField(label="Manager's Email", required=True)
