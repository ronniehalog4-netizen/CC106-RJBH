from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_registration, name='student_registration'),
<<<<<<< HEAD
    path('register/', views.student_registration, name='register'),
    path('success/', views.registration_success, name='registration_success'),
    path('students/', views.student_list, name='student_list'),
    path('students/create/', views.student_create, name='student_create'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/<int:pk>/edit/', views.student_update, name='student_update'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),
=======
    path('success/', views.registration_success, name='registration_success'),
>>>>>>> 4e2095b301e79c53a3163efbac07279351819274
]