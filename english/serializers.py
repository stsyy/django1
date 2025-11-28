from rest_framework import serializers
from english.models import Student, Test, TestQuestion, Result, TestQuestionVariant, Tutor

class StudentSerializer(serializers.ModelSerializer):
    picture_url = serializers.SerializerMethodField()
    class Meta:
        model = Student
        fields = ('id', 'name', 'level', 'progress', 'picture', 'user', 'picture_url')
        
    def create(self, validated_data):
        if 'request' in self.context and hasattr(self.context['request'], 'user'):

            validated_data['user'] = self.context['request'].user
        
        return super().create(validated_data)

    def get_picture_url(self, obj):
        if obj.picture:
            return obj.picture.url
        return None
    
class TutorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Tutor
        fields = ['id', 'user', 'username', 'name']
        read_only_fields = ['user']    

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