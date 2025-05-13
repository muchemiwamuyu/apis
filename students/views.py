from django.shortcuts import render
from django.http import HttpResponse
from .models import Student, Course
from .serializers import StudentSerializer, CourseSerializer
from rest_framework import viewsets

# Create your views here.


def index(request):

    return HttpResponse('My app is running')

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

