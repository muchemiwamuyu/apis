from django.db import models

# Create your models here.
class Student(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Prefer not to say'),
    )
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='N')
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    location = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Course(models.Model):
    course_name = models.CharField(max_length=50)
    course_description = models.CharField(max_length=50)
    duration_date = models.IntegerField()

    def __str__(self):
        return self.course_name
