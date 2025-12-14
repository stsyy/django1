from rest_framework.permissions import BasePermission


class CanSeePage1Permission(BasePermission):
    message = "нельзя это делать" 
    def has_permission(self, request, view):

        return request.user.has_perm('general.can_see_page1')
    

class SecondFactorPermission(BasePermission):
    message = "нельзя это делать" 
    def has_permission(self, request, view):
        return request.session.get('second') == True