from django.urls import path
from .views import get_current_course_lesson, LoginView, RegisterView

urlpatterns = [
    path('get_current_course_lesson/', get_current_course_lesson),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]