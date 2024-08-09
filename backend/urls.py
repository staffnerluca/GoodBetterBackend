from django.urls import path
from .views import get_current_course_lesson, get_eating_meat_days, login_view, register, create_test_users, get_all_users, create_test_days

urlpatterns = [
    path('get_current_course_lesson/', get_current_course_lesson),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('get_meat_days/', get_eating_meat_days, name='get_meat_days'),
    path('create_test_users/', create_test_users, name='create_test_users'),
    path('get_all_users/', get_all_users, name='get_all_users'),
    path('create_test_days/', create_test_days, name='create_test_days')
]