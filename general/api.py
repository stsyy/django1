import pyotp
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth import authenticate, login, logout
from .serializers import UserProfileSerializer
from general.models import UserProfile
import time

"""
/users/ GET
/users/ POST
/users/1/ GET 
/users/1/ UPDATE
/users/my/ detail = False
/users/login/ detail = False
/users/1/my/ detail = True
"""


class UserProfileViewSet(GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    @action(url_path="my", methods=["GET"], detail=False)
    def get_my(self, request, *args, **kwargs):
        permissions = self.request.user.get_all_permissions()
        data = {
            'username': self.request.user.username,
            'is_authenticated': self.request.user.is_authenticated,
            'is_staff': self.request.user.is_staff,
            'can_see_all_students': self.request.user.has_perm('general.can_see_all_students'),
    
            #'can_create_students': self.request.user.has_perm('general.can_create_students'),
            #'can_update_students': self.request.user.has_perm('general.can_update_students'),
            #'can_delete_students': self.request.user.has_perm('general.can_delete_students'),
            'can_see_himself': self.request.user.has_perm('general.can_see_himself'),

            'can_see_test_questions': self.request.user.has_perm('general.can_see_test_questions'),
            'can_create_test_questions': self.request.user.has_perm('general.can_create_test_questions'),
            'can_update_test_questions': self.request.user.has_perm('general.can_update_test_questions'),
            'can_delete_test_questions': self.request.user.has_perm('general.can_delete_test_questions'),

            'can_see_test_question_variants': self.request.user.has_perm('general.can_see_test_question_variants'),
            'can_create_test_question_variants': self.request.user.has_perm('general.can_create_test_question_variants'),
            'can_update_test_question_variants': self.request.user.has_perm('general.can_update_test_question_variants'),
            'can_delete_test_question_variants': self.request.user.has_perm('general.can_delete_test_question_variants'),

            'can_see_all_results': self.request.user.has_perm('general.can_see_all_results'),
            'can_see_own_results': self.request.user.has_perm('general.can_see_own_results'),

            'can_see_all_tutors': self.request.user.has_perm('general.can_see_all_tutors'),
            'can_see_his_tutor': self.request.user.has_perm('general.can_see_his_tutor'),
            'can_create_tutors': self.request.user.has_perm('general.can_create_tutors'),
            'can_update_tutors': self.request.user.has_perm('general.can_update_tutors'),
            'can_delete_tutors': self.request.user.has_perm('general.can_delete_tutors'),
            
            'can_see_stats': self.request.user.has_perm('general.can_see_stats'),
            
            'permissions': permissions
        }

        if self.request.user.is_authenticated:
            data.update({
                #сюда добавить разрешение по которому 2фактор (это МОЙ КОММЕНТ ДЛЯ МЕНЯ)
                'can_create_students': self.request.user.has_perm('general.can_create_students'),
                'can_update_students': self.request.user.has_perm('general.can_update_students'),
                'can_delete_students': self.request.user.has_perm('general.can_delete_students'),
                'second': self.request.session.get('second') or False,
            })

        return Response(data)
    @action(detail=False, methods=['GET'], url_path='tutors')
    def tutors(self, request):
        if not request.user.is_superuser:
            return Response({"error": "Только суперюзер может просматривать преподавателей"}, status=403)

        qs = self.get_queryset().filter(type='tutor')
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
    
    @action(url_path="login", methods=["POST"], detail=False)
    def process_login(self, *args, **kwargs):
        class LoginSerializer(serializers.Serializer):
            username = serializers.CharField()
            password = serializers.CharField()

        serializer = LoginSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)
        if user:
            login(self.request, user)
        else:
            return Response({
                "status": "failed"
            }, status=401)

        return Response({
            "status": "success"
        })
    
    @action(url_path="logout", methods=['POST'], detail=False)
    def process_logout(self, *args, **kwargs):
        logout(self.request)

        return Response({
            "status": "success"
        })
    
    @action(url_path="get-totp", methods=['GET'], detail=False)
    def get_totp(self, *args, **kwargs):
        self.request.user.userprofile.totp_key = pyotp.random_base32()
        self.request.user.userprofile.save()

        url = pyotp.totp.TOTP(self.request.user.userprofile.totp_key).provisioning_uri(
            name=self.request.user.username, issuer_name="MyApp"
        )

        return Response({
            "url": url
        })
    
    
    @action(url_path="second-login", methods=['POST'], detail=False)
    def second_login(self, *args, **kwargs):
        key = self.request.user.userprofile.totp_key
        t = pyotp.totp.TOTP(key)
        key = self.request.data.get('key')
        if key == t.now():
            self.request.session['second'] = {
                "active": True,
                "expires": time.time()+60
            }
        return Response({
            "status": "success",
            "second": self.request.session.get("second")
        })