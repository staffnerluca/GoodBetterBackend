from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json
from .models import UserProfile
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, LoginSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            password = serializer.data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#course logic for the user
def get_current_course_lesson(request):
    return JsonResponse({"basicMorality": "10"})

def check_login(request):
    pass
 
# Creating stuff
def register_user(request):
    pass

def create_course():
    pass

def create_good_thing():
    pass

# Update
def update_user_moral_alignment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ci = data["categorical_imperative"]
            ut = data["utilitarian"]
            ve = data["virute_ethics"]
            ar = data["animal_rights"]
            lo = data["longtermism"]
            user_id = data["user_id"]
            user = get_object_or_404(UserProfile, id=user_id)
            user.categorical_imperative = ci
            user.utilitarian = ut
            user.virute_ethics = ve
            user.animal_rights = ar
            user.longtermism =  lo
            user.save()
        except json.JSONDecodeError:
            return JsonResponse({"error": "Inavalid JSOn"}, status = 400)
        