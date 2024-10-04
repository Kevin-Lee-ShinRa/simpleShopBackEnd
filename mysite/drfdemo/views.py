from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from drfdemo import sers
from drfdemo.models import Student
from drfdemo.sers import StudentModelSerializer


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer


