from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from english.models import Student, Test, TestQuestion, Result, TestQuestionVariant, Tutor




    
class TutorSerializer(serializers.ModelSerializer):
    #username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Tutor
        fields = ['id', 'user', 'username', 'name']  

class TestQuestionVariantSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)    
    class Meta:
        model = TestQuestionVariant
        fields = '__all__'

class TestQuestionSerializer(serializers.ModelSerializer):
    #picture_url = serializers.SerializerMethodField()
    #test_name = serializers.CharField(source='test.name', read_only=True)
    variants = TestQuestionVariantSerializer(many=True, read_only=True)
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)    
    class Meta:
        model = TestQuestion
        fields = '__all__'   
        

class TestSerializer(serializers.ModelSerializer):
    questions = TestQuestionSerializer(many=True, read_only=True)
    class Meta:
        model = Test
        fields = '__all__'
class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'
        
class StudentSerializer(serializers.ModelSerializer):
    tutor_name = serializers.SerializerMethodField()
    assigned_tests = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Test.objects.all(),
        write_only=True
    )
    assigned_tests_info = TestSerializer(
        many=True,
        source='assigned_tests',
        read_only=True
    )

    def create(self, validated_data):
        request = self.context['request']
        if not request.user.is_superuser:
            validated_data.pop('tutor', None)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context['request']
        if not request.user.is_superuser:
            validated_data.pop('tutor', None)
        return super().update(instance, validated_data)

    def get_tutor_name(self, obj):
        return obj.tutor.userprofile.name if obj.tutor and hasattr(obj.tutor, 'userprofile') else None  

    class Meta:
        model = Student
        fields = '__all__'

class StatsSerializer(serializers.Serializer):
    count = serializers.IntegerField(required=False)
    avg = serializers.FloatField(required=False)
    min = serializers.FloatField(required=False)
    max = serializers.FloatField(required=False)