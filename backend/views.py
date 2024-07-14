from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
import json
from .models import UserProfile


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            # Erfolgreich eingeloggt
            return JsonResponse({'message': 'Login erfolgreich'})
        else:
            # Ungültige Anmeldeinformationen
            return JsonResponse({'error': 'Ungültige Anmeldeinformationen'}, status=400)

    # Falls GET- oder anderer Request-Methode
    return JsonResponse({'error': 'Methode nicht erlaubt'}, status=405)
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
        