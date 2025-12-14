from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from english.models import Student, Test, TestQuestion, Result, TestQuestionVariant, Tutor

class StudentSerializer(serializers.ModelSerializer):
    #picture_url = serializers.SerializerMethodField()
    class Meta:
        model = Student
        fields = '__all__'
    
class TutorSerializer(serializers.ModelSerializer):
    #username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Tutor
        fields = ['id', 'user', 'username', 'name']  

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'

class TestQuestionSerializer(serializers.ModelSerializer):
    #picture_url = serializers.SerializerMethodField()
    #test_name = serializers.CharField(source='test.name', read_only=True)
    class Meta:
        model = TestQuestion
        fields = '__all__'   
        
class TestQuestionVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestQuestionVariant
        fields = '__all__'

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'