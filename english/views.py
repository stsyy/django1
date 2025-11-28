# english/views.py

from django.db.models import Count, Avg, Max, Min, Sum, Q # Импортируем Q для фильтрации
from django.contrib.auth import logout, authenticate, login
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

# Импорты моделей и сериализаторов
from english.models import Student, Test, TestQuestion, TestQuestionVariant, Result, Tutor
from .serializers import StudentSerializer, TestQuestionSerializer, TestSerializer, ResultSerializer, TestQuestionVariantSerializer # Убедись, что все сериализаторы здесь

# --- 1. АУТЕНТИФИКАЦИОННЫЕ ФУНКЦИИ ---

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return Response({
            'detail': 'Успешный вход.', 
            'username': user.username
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'detail': 'Неверный логин или пароль.'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny]) 
def user_status_view(request):
    """
    Возвращает данные о текущем аутентифицированном пользователе и его роль.
    """
    user = request.user
    role = 'Гость'
    
    if user.is_authenticated:
        if user.is_superuser:
            role = 'Администратор'
        elif is_tutor(user):
            role = 'Репетитор'
        # Если не суперюзер и не репетитор, считаем, что это Студент (из-за логики фильтрации в get_queryset)
        else: 
            # Дополнительная проверка, что это именно Студент, если нужно
            if Student.objects.filter(user=user).exists():
                role = 'Студент'
            else:
                role = 'Пользователь' # Для пользователей без Student/Tutor профиля
        
        return Response({
            'isLoggedIn': True,
            'username': user.username,
            'id': user.id,
            'role': role, # <-- Ключевое поле для фронтенда
            'is_superuser': user.is_superuser
        })
    else:
        return Response({
            'isLoggedIn': False,
            'username': None,
            'id': None,
            'role': role,
            'is_superuser': False
        })


@api_view(['POST']) 
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Сбрасывает сессию пользователя."""
    logout(request)
    return Response({'detail': 'Успешный выход из системы.'}, status=status.HTTP_200_OK)

def is_tutor(user):
    """Проверяет, является ли пользователь репетитором, проверяя наличие профиля Tutor."""
    # Если пользователь не аутентифицирован, он точно не репетитор
    if not user.is_authenticated:
        return False
        
    try:
        # Пытаемся получить связанный профиль Tutor
        return Tutor.objects.filter(user=user).exists()
    except Tutor.DoesNotExist:
        return False

# --- 2. VIEWSETS С ЛОГИКОЙ И СТАТИСТИКОЙ ---

class StudentsViewset(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated] # Используем permission_classes

    def get_queryset(self):
        user = self.request.user
        
        # 1. Администратор и Репетитор видят всех студентов
        if user.is_superuser or is_tutor(user):
            return Student.objects.all()
        
        # 2. Студент видит только себя
        else:
            return Student.objects.filter(user=user)
        
    def get_permissions(self):
        # Запрет на CRUD для студентов.
        # Разрешаем только чтение (GET, HEAD, OPTIONS) для не-админов/не-репетиторов
        if not self.request.user.is_superuser and not is_tutor(self.request.user):
            if self.action in ['create', 'update', 'partial_update', 'destroy']:
                # Используем ReadOnly, чтобы явно запретить изменение
                return [permission() for permission in [permissions.IsAuthenticatedOrReadOnly] if self.request.method not in permissions.SAFE_METHODS]
                
        return super().get_permissions()    
    
    # МЕТОД СТАТИСТИКИ ДЛЯ СТУДЕНТОВ
    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        stats = queryset.aggregate(
            total_students=Count("id"),
            avg_progress=Avg("progress"), 
            max_progress=Max("progress"), 
            min_progress=Min("progress"),
        ) 
        return Response(stats)

class TestQuestionViewSet(viewsets.ModelViewSet):
    serializer_class = TestQuestionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return TestQuestion.objects.all()
        else:
            # Студенты обычно не видят список вопросов
            return TestQuestion.objects.none()
    
    # МЕТОД СТАТИСТИКИ ДЛЯ ВОПРОСОВ
    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        stats = queryset.aggregate(
            total_questions=Count("id"),
            # Здесь можно добавить другие агрегаты
        )
        return Response(stats)
    
class TestViewSet(viewsets.ModelViewSet):
    serializer_class = TestSerializer 
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Test.objects.all()
        else:
            return Test.objects.filter(user=user)

    # МЕТОД СТАТИСТИКИ ДЛЯ ТЕСТОВ
    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        stats = queryset.aggregate(
            total_tests=Count("id"),
            # Среднее количество вопросов в тесте (посчитанное через обратную связь)
            avg_questions_per_test=Avg('testquestion__id', default=0) 
        )
        return Response(stats)
    
class TestQuestionVariantViewSet(viewsets.ModelViewSet):
    serializer_class = TestQuestionVariantSerializer 
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return TestQuestionVariant.objects.all()
        else:
            return TestQuestionVariant.objects.filter(user=user)

    # МЕТОД СТАТИСТИКИ ДЛЯ ВАРИАНТОВ
    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        stats = queryset.aggregate(
            total_variants=Count("id"),
            # Считаем количество правильных ответов с помощью Q-объекта
            correct_variants_count=Count("id", filter=Q(is_corect=True)) 
        )
        return Response(stats) 
    
class ResultViewSet(viewsets.ModelViewSet):
    serializer_class = ResultSerializer 
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Result.objects.all()
        else:
            # Студенты видят только свои результаты, связанные с их студенческим профилем
            try:
                current_student = Student.objects.get(user=user)
                return Result.objects.filter(student=current_student)
            except Student.DoesNotExist:
                return Result.objects.none()

    # МЕТОД СТАТИСТИКИ ДЛЯ РЕЗУЛЬТАТОВ
    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        stats = queryset.aggregate(
            total_results=Count("id"),
            avg_score=Avg("score"), 
            max_score=Max("score"), 
            min_score=Min("score"),
            total_score_sum=Sum("score")
        )
        return Response(stats)