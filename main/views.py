from django.shortcuts import render , redirect
from django.contrib.auth import logout
from courses.models import Course 

def home(request):
    courses = Course.objects.all()[:6] 
    return render(request,'accounts/home.html', {'courses': courses})

