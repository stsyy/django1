import pyotp
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth import authenticate, login, logout

from general.models import UserProfile


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

    @action(url_path="my", methods=["GET"], detail=False)
    def get_my(self, *args, **kwargs):
        permissions = self.request.user.get_all_permissions()
        data = {
            'username': self.request.user.username,
            'is_authenticated': self.request.user.is_authenticated,
            'is_staff': self.request.user.is_staff,
            'can_create_students': self.request.user.has_perm('general.can_create_students'),
            'can_see_test_questions': self.request.user.has_perm('general.can_see_test_questions'),
            'can_see_all_students': self.request.user.has_perm('general.can_see_all_students'),
            'can_see_all_results': self.request.user.has_perm('general.can_see_all_results'),
            'permissions': permissions
        }

        if self.request.user.is_authenticated:
            data.update({
                'can_see_test_questions': self.request.user.userprofile.can_see_test_questions,
                'second': self.request.session.get('second') or False,
            })

        return Response(data)

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
            self.request.session['second'] = True;

        return Response({
            "status": "success"
        })