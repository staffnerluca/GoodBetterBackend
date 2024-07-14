from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=30)
    second_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    country = models.CharField(max_length=2) #only country code
    age = models.IntegerField()
    isAdmin = models.BooleanField()

    #moral alignment in %
    categorical_imperative = models.IntegerField()
    utilitarian = models.IntegerField()
    virute_ethics = models.IntegerField()
    animal_rights = models.IntegerField()
    longtermism = models.IntegerField()

    wants_to_become_vegetarian = models.BooleanField()
    doing_good_streak = models.IntegerField()
    not_eating_meat_streak = models.IntegerField()
    course_streak = models.IntegerField()
    joined_at = models.DateField()
    total_time_on_the_app_in_minutes = models.BigIntegerField()
    total_amount_of_donations = models.IntegerField()
    donations_per_week_goal = models.IntegerField()
    #the days a person wants to eat meat. For example if it is monday and friday MoFr
    meat_days = models.CharField(max_length=12)
    goodness_score = models.IntegerField()


class Course(models.Model):
    name = models.CharField(max_length=50)
    creator = models.IntegerField() #id of the creator
    goal = models.TextField()
    moral_type = models.CharField() # is there a school of thought that is presented in this course
    course_type = models.CharField(max_length=2)


class CourseQuestion(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()
    goal = models.TextField()
    creator = models.IntegerField()
    #defines for which moral groups this can be relevant
    relevant_for = models.CharField(20)
    interactive = models.BooleanField()
    #multiple choice quizes are stored with a special syntax in content
    multiple_choice_quiz = models.BooleanField()
    info_screen = models.BooleanField()
    image = models.ImageField()
    furhter_resources = models.TextField()


class GoodThing(models.Modle):
    name = models.CharField(max_length=100)
    impact = models.CharField(max_length=200)
    creator = models.CharField(max_length=20)
    #defines for which moral groups this can be relevant
    relevant_for = models.CharField(20)


class Issues(models.Model):
    issue_name = models.CharField()


class DoneGoodThings(models.Model):
    user = models.IntegerField()
    good_thing = models.IntegerField()


class DoneQuestions(models.Model):
    user = models.IntegerField()
    course_question = models.IntegerField()


"""
could be determined by the done Course Questions but if they change a finished course would be shown to be unfinished
and it just saves server side calculation power to do it that way for a very moderate cost in memory
"""
class DoneCourses(models.Model):
    user = models.IntegerChoices()
    coures = models.IntegerField()


class DoingGoodNetworkPost():
    creator = models.IntegerField()
    content = models.TextField()
    post_date = models.DateField()
    # is it a comment to an other post if yes to which?
    commentsOn = models.IntegerField()
    violates_conde_of_conduct = models.BooleanField()


class LikedPosts(models.Model):
    post = models.IntegerField()
    user = models.IntegerField()