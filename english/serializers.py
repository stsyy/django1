from rest_framework import serializers
from english.models import Student, Result

class ResultSeializer(serializers.ModelSerializer):
    class Meta:
        model=Result
        fields="__all__"

class StudentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Student
        fields=['id','name','login','level','progress']