from rest_framework import serializers
from english.models import Student, Word, Test, Result, Lesson

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model=Result
        fields="__all__"

class StudentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Student
        fields=['id','name','login','level','progress']

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = '__all__'

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'
        
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'      
