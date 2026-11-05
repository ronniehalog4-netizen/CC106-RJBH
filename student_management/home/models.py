from django.db import models

# Create your models here.
<<<<<<< HEAD
=======

>>>>>>> 4e2095b301e79c53a3163efbac07279351819274
class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100, null=True, blank=True)
<<<<<<< HEAD
    
=======
   
>>>>>>> 4e2095b301e79c53a3163efbac07279351819274
