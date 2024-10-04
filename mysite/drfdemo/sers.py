# from django.db.migrations import serializer

from rest_framework import serializers

from drfdemo.models import Student


class StudentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
