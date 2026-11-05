from django.db import models

# Create your models here.
<<<<<<< HEAD
class student(models.Model):
    GENDER_CHOICES = [
=======
class Student(models.Model):
    GENDER_CHOICES =[
>>>>>>> 4e2095b301e79c53a3163efbac07279351819274
        ('Male', 'Male'),
        ('Female', 'Female')
    ]

<<<<<<< HEAD
    student_id=models.CharField(
        max_length=20,
        unique=True)

    first_name=models.CharField(
        max_length=100)

    last_name=models.CharField(
        max_length=100)

    gender=models.CharField(
        max_length=10,
        choices=GENDER_CHOICES)

    date_of_birth=models.DateField()

    contact_number=models.CharField(
        max_length=20)

    def __str__(self):
        return f"{self.student_id} - {self.first_name} {self.last_name}"
    
=======
    student_id = models.CharField(
        max_length=20, 
        unique=True)
    first_name = models.CharField(
        max_length=100)
    
    last_name = models.CharField(
        max_length=100)

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES)

    date_of_birth = models.DateField()

    contact_number = models.CharField(
        max_length=20)
    def __str__(self):
        return f"{self.student_id} - {self.first_name} {self.last_name}"
>>>>>>> 4e2095b301e79c53a3163efbac07279351819274
