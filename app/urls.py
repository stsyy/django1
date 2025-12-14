from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from general.api import UserProfileViewSet
from debug_toolbar.toolbar import debug_toolbar_urls

from english import views
from rest_framework.routers import DefaultRouter

from english.api import StudentsViewSet, TestsViewSet, ResultsViewSet, TestQuestionsViewSet
#from english.api import StudentsViewset, TestsViewset, TestQuestionsViewset, ResultsViewset

router = DefaultRouter()
router.register("students", StudentsViewSet, basename="student")
router.register("tests", TestsViewSet, basename="test")
router.register("results", ResultsViewSet, basename="result") 
#router.register("test_question_variants", TestQuestionVariantViewSet, basename='testquestionvariant')
router.register("test_questions", TestQuestionsViewSet, basename="testquestion")
#router.register("tutors", TutorsViewSet, basename="tutor")
router.register('users', UserProfileViewSet, basename='users')

urlpatterns = [
    #path("students", views.StudentsListTemplate.as_view()),
   # path('', views.ShowStudentsView.as_view()),
    path("admin/", admin.site.urls),
    path('api/', include(router.urls)),
    #path('api/login/', login_view, name='login'),
    #path('api/user/status/', user_status_view, name='user_status'),
    #path('api/logout/', logout_view, name='logout'),
]   +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
