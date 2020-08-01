from django import forms
from bigbenapp.models import Post, Appointment, DateTimeTest

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']

#

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class TextInput(forms.TextInput):
    input_type = 'blaze'


#

class DateForm(forms.Form):
    date = forms.DateTimeField(widget=DateInput)

class DateModelForm(forms.ModelForm):
    class Meta:
        model = DateTimeTest
        fields = {'date', }
        widget = {'date': DateInput()}

#

class ApointmentForm(forms.Form):
    blaze = forms.CharField(widget=TextInput)
    email = forms.CharField(widget=TextInput)
    date = forms.DateField(widget=DateInput)
    time = forms.TimeField(widget=TimeInput)

class ApointmentModelForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['blaze', 'email' ,'date', 'time']
        widget = { 'blaze': TextInput, 'email':forms.EmailField(widget=TextInput) ,'date': forms.DateField(widget=DateInput), 'time': forms.TimeField(widget=TimeInput)}

class AppointmentUpdateForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['confirmed']