from django.shortcuts import render , redirect
from django.contrib.auth import logout
from courses.models import Course 

def home(request):
<<<<<<< HEAD
    if request.user.is_authenticated:
        courses = Course.objects.all()
        return render(request, 'main/dashboard.html', {'courses': courses})
    else:
        courses = Course.objects.all()[:3] 
        return render(request, 'main/home.html', {'courses': courses})
    
def about_us(request):
    return render(request, 'main/about_us.html')
=======
    courses = Course.objects.all()[:6] 
    return render(request,'accounts/home.html', {'courses': courses})

>>>>>>> 0306852464c31f547468529447e570b6a5fb907c
