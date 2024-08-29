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


class CourseQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseQuestion
        fields = [
            'id', 
            'name', 
            'content', 
            'image', 
            'course', 
            'is_boolean', 
            'options', 
            'next_question_if_true', 
            'next_question_if_false', 
            'is_first'
        ]


class CourseSerializer(serializers.ModelSerializer):
    imageUrl = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'
        fields = ['id', 'name', 'goal', 'imageUrl']

    def get_imageUrl(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.image) if obj.image else ''


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