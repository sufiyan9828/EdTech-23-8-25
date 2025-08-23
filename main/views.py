# MainProject/main/views.py
from django.shortcuts import render , redirect
from django.contrib.auth import logout
from courses.models import Course # Import Course model

def home(request):
    # Fetch some courses to display on the main homepage
    courses = Course.objects.all()[:6] # Example: show first 6 courses
    return render(request,'accounts/home.html', {'courses': courses}) # Pass courses as 'courses'
