from rest_framework import serializers
from .models import CustomUser, Course, UserProfile, Days, CourseQuestion, DoneQuestions, DoneCourses

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email_address', 'username', 'first_name', 'last_name']


class UserProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'first_name', 'second_name', 'username', 
            'country', 'birth_date', 'isAdmin', 'wants_to_become_vegetarian', 
            'not_eating_meat_streak', 'course_streak', 'joined_at', 
            'total_time_on_the_app_in_minutes', 'meat_days'
        ]


class DaysSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = Days
        fields = ['id', 'user', 'date', 'vegetarian_status']


class CourseSerializer(serializers.ModelSerializer):
    creator = UserProfileSerializer()

    class Meta:
        model = Course
        fields = ['id', 'name', 'creator', 'goal', 'moral_type', 'course_type']


class CourseQuestionSerializer(serializers.ModelSerializer):
    creator = UserProfileSerializer()

    class Meta:
        model = CourseQuestion
        fields = [
            'id', 'name', 'content', 'goal', 'creator', 
            'relevant_for', 'interactive', 'multiple_choice_quiz', 
            'info_screen', 'image', 'furhter_resources'
        ]


class DoneQuestionsSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    course_question = CourseQuestionSerializer()

    class Meta:
        model = DoneQuestions
        fields = ['id', 'user', 'course_question']


class DoneCoursesSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    course = CourseSerializer()

    class Meta:
        model = DoneCourses
        fields = ['id', 'user', 'course']