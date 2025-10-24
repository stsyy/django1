from rest_framework import serializers
from english.models import Student, Test, TestQuestion, Result, TestQuestionVariant

class StudentSerializer(serializers.ModelSerializer):
    picture_url = serializers.SerializerMethodField()
    class Meta:
        model = Student
        fields = '__all__'
        
    def get_picture_url(self, obj):
        if obj.picture:
            return obj.picture.url
        return None

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'

class TestQuestionSerializer(serializers.ModelSerializer):
    picture_url = serializers.SerializerMethodField()
    test_name = serializers.CharField(source='test.name', read_only=True)
    class Meta:
        model = TestQuestion
        fields = '__all__'
    def get_picture_url(self, obj):
        if obj.picture:
            return obj.picture.url
        return None    
        
class TestQuestionVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestQuestionVariant
        fields = '__all__'

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'