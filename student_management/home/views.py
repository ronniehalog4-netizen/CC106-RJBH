from django.shortcuts import render

# Create your views here.
def landing(request):
    return render(request, 'home/landing.html')

def home(request):
<<<<<<< HEAD
    return render(request, 'home/home.html')
=======
    return render(request, 'home/home.html')
>>>>>>> 4e2095b301e79c53a3163efbac07279351819274
