from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
<<<<<<< HEAD
    path('home/', views.home, name='home'),
=======
    path('Home/', views.home, name='home'),
>>>>>>> 4e2095b301e79c53a3163efbac07279351819274
]