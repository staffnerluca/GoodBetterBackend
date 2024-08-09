from .models import Days, UserProfile
from django.db import transaction
from django.utils import timezone
import random

for i in range(10):
    user_profile = UserProfile.objects.get(username="username1")
    with transaction.atomic():
        for i in range(30):
            day = timezone.now().date() - timezone.timedelta(days = i)
            vegetarian_status = random.choice(["v", "m", "f"])
            Days.objects.create(
                user = user_profile,
                date = day,
                vegetarian_status = vegetarian_status
            )
print("Created days")