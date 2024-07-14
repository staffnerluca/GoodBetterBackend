from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json
from .models import UserProfile

#course logic for the user
def get_current_course_lesson(request):
    return JsonResponse({"basicMorality": "10"})


# Creating stuff
def create_user():
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
        