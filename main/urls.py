from django.urls import path    
from . import views
from .views import *
urlpatterns = [
<<<<<<< HEAD
    path('',views.home,name="home"),
    path('about-us/', views.about_us, name='about_us'),
=======
    path('',views.home,name="home")
>>>>>>> 0306852464c31f547468529447e570b6a5fb907c
]
