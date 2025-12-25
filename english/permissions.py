from rest_framework.permissions import BasePermission
import time

#class CanSeePage1Permission(BasePermission):
 #   message = "нельзя это делать" 
  #  def has_permission(self, request, view):

   #     return request.user.has_perm('general.can_see_page1')
    
#пока закомменчу
#class SecondFactorPermission(BasePermission):
 #   message = "нельзя это делать" 
  #  def has_permission(self, request, view):
   #     return request.session.get('second') == True  
   
class CanSeeAllStudentsPermission(BasePermission):
    message = "У вас нет права на просмотр всех студентов."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_perm('general.can_see_all_students')     
    
class CanCreateStudentsPermission(BasePermission):
    message = "У вас нет права на создание студентов."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_perm('general.can_create_students')
    
class CanDeleteStudentsPermission(BasePermission):
    message = "У вас нет права на удаление студентов."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return  request.user.has_perm('general.can_delete_students')   
    
class CanUpdateStudentsPermission(BasePermission):
    message = "У вас нет права на редактирование студентов."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return  request.user.has_perm('general.can_update_students')  

class CanSeeHimselfPermission(BasePermission):
    message = "У вас нет права на просмотр себя?"
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_perm('general.can_see_himself')          
    
class CanSeeTestQuestionsPermission(BasePermission):
    message = "У вас нет права на просмотр вопросов тестов."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_perm('general.can_see_test_questions')
    
class CanCreateTestQuestionsPermission(BasePermission):
    message = "У вас нет права на создание вопросов тестов."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_perm('general.can_create_test_questions')    
    
class CanDeleteTestQuestionsPermission(BasePermission):
    message = "У вас нет права на удаление вопросов тестов."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_perm('general.can_delete_test_questions')    
    
class CanUpdateTestQuestionsPermission(BasePermission):
    message = "У вас нет права на редактирование вопросов тестов."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_perm('general.can_update_test_questions')     
    
class CanSeeTestQuestionsVariantsPermission(BasePermission):
    message = "У вас нет права на просмотр вариантов вопросов тестов."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_perm('general.can_see_test_questions_variants') 
    
class CanCreateTestQuestionsVariantsPermission(BasePermission):
    message = "У вас нет права на create вариантов вопросов тестов."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_perm('general.can_create_test_questions_variants')     
    
class CanDeleteTestQuestionsVariantsPermission(BasePermission):
    message = "У вас нет права на удаление вариантов вопросов тестов."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_perm('general.can_delete_test_questions_variants') 
    
class CanUpdateTestQuestionsVariantsPermission(BasePermission):
    message = "У вас нет права на редактирование вариантов вопросов тестов."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_perm('general.can_update_test_questions_variants')            
    
class CanSeeAllResultsPermission(BasePermission):
    message = "У вас нет права на просмотр всех результатов."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_perm('general.can_see_all_results')     
    
class CanSeeOwnResultPermission(BasePermission):
    message = "У вас нет права на просмотр своих результатов."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_perm('general.can_see_own_results')               
    
class CanSeeAllTutorsPermission(BasePermission):
    message = "У вас нет права на просмотр всех преподавателей."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_perm('general.can_see_all_tutors')  
    
class CanCreateTutorsPermission(BasePermission):
    message = "У вас нет права на добавление преподавателей."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_perm('general.can_create_tutors')  
    
class CanDeleteTutorsPermission(BasePermission):
    message = "У вас нет права на удаление преподавателей."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_perm('general.can_delete_tutors')   
    
class CanUpdateTutorsPermission(BasePermission):
    message = "У вас нет права на редактирование преподавателей."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_perm('general.can_update_tutors')       
              
class CanSeeHisTutorPermission(BasePermission):
    message = "У вас нет права на просмотр преподавателя."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_perm('general.can_see_his_tutor')  
    
class CanSeeStats(BasePermission):
    message = "У вас нет права на просмотр статистики."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_perm('general.can_see_stats')      
    
class SecondFactorPermission(BasePermission):
    def has_permission(self, request, view):
        second = request.session.get("second")
        if not second or not second.get("active"):
            return False
        
        if time.time() > second["expires"]:
            request.session["second"] = None
            request.session.modified = True
            return False

        return True              
               