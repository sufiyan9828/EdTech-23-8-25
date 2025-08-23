from django.forms import ModelForm
from django import forms
from .models import Course, Enrollment 

class CoursePostingForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'category', 'price', 'start_date', 'end_date','image']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'image': forms.FileInput(attrs={'accept': 'image/*'}),
        }

class EnrollmentForm(ModelForm):
    class Meta:
        model = Enrollment
        fields = ['notes'] 
