from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, StudentProfile, InstructorProfile  
from django import forms


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'contact', 'user_type']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=25)
    password = forms.CharField(max_length=25, widget=forms.PasswordInput)


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile  
<<<<<<< HEAD
        fields = ['educations', 'institution_name', 'current_year', 'student_id', 'profile_photo']
=======
        fields = ['educations', 'skills', 'experience', 'resume', 'profile_photo']
>>>>>>> 0306852464c31f547468529447e570b6a5fb907c
        widgets = {
            'profile_photo': forms.FileInput(attrs={'accept': 'image/*'}),
        }


class InstructorProfileForm(forms.ModelForm):
    class Meta:
        model = InstructorProfile  
        fields = ['organization_name', 'contact', 'profile_photo']  
        widgets = {
            'profile_photo': forms.FileInput(attrs={'accept': 'image/*'}),
        }
<<<<<<< HEAD
=======

>>>>>>> 0306852464c31f547468529447e570b6a5fb907c
