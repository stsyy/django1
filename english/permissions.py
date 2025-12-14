from rest_framework.permissions import BasePermission


#class CanSeePage1Permission(BasePermission):
 #   message = "нельзя это делать" 
  #  def has_permission(self, request, view):

   #     return request.user.has_perm('general.can_see_page1')
    
#пока закомменчу
#class SecondFactorPermission(BasePermission):
 #   message = "нельзя это делать" 
  #  def has_permission(self, request, view):
   #     return request.session.get('second') == True
   
class CanSeeAllStudents(BasePermission):
    message = "У вас нет права на просмотр всех студентов."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.is_staff or request.user.is_superuser or request.user.has_perm('general.can_see_all_students')     
    
class CanCreateStudents(BasePermission):
    message = "У вас нет права на создание студентов."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_perm('general.can_create_students')
    
class CanDeleteStudents(BasePermission):
    message = "У вас нет права на удаление студентов."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_perm('general.can_delete_students')   
    
class CanUpdateStudents(BasePermission):
    message = "У вас нет права на редактирование студентов."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_perm('general.can_update_students')      
    
class CanSeeTestQuestions(BasePermission):
    message = "У вас нет права на просмотр вопросов тестов."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_perm('general.can_see_test_questions_variants')
    
class CanCreateTestQuestions(BasePermission):
    message = "У вас нет права на создание вопросов тестов."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_perm('general.can_create_test_questions_variants')    
    
class CanDeleteTestQuestions(BasePermission):
    message = "У вас нет права на удаление вопросов тестов."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_perm('general.can_delete_test_questions_variants')    
    
class CanUpdateTestQuestions(BasePermission):
    message = "У вас нет права на редактирование вопросов тестов."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_perm('general.can_update_test_questions_variants')     
    
class CanSeeTestQuestionsVariants(BasePermission):
    message = "У вас нет права на просмотр вариантов вопросов тестов."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_perm('general.can_see_test_questions') 
    
class CanDeleteTestQuestionsVariants(BasePermission):
    message = "У вас нет права на удаление вариантов вопросов тестов."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_perm('general.can_delete_test_questions') 
    
class CanUpdateTestQuestionsVariants(BasePermission):
    message = "У вас нет права на редактирование вариантов вопросов тестов."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_perm('general.can_update_test_questions')            
    
class CanSeeAllResults(BasePermission):
    message = "У вас нет права на просмотр всех результатов."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.is_staff or request.user.is_superuser or request.user.has_perm('general.can_see_all_results')              
    
class CanSeeAllTutors(BasePermission):
    message = "У вас нет права на просмотр всех преподавателей."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.is_staff or request.user.is_superuser or request.user.has_perm('general.can_see_all_tutors')  
    
class CanCreateAllTutors(BasePermission):
    message = "У вас нет права на добавление преподавателей."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.is_staff or request.user.is_superuser or request.user.has_perm('general.can_create_tutors')  
    
class CanDeleteAllTutors(BasePermission):
    message = "У вас нет права на удаление преподавателей."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.is_staff or request.user.is_superuser or request.user.has_perm('general.can_delete_tutors')   
    
class CanUpdateAllTutors(BasePermission):
    message = "У вас нет права на редактирование преподавателей."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.is_staff or request.user.is_superuser or request.user.has_perm('general.can_update_tutors')       
              