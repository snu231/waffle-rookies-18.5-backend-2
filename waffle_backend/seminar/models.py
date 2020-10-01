from django.contrib.auth.models import User

from django.db import models

# Create your models here.

class Seminar(models.Model):
    name = models.CharField(max_length=50)

    joined_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField()    #

    dropped_at = models.DateTimeField(auto_now=True)

    # sem = SeminarManager()
    # users = models.ManyToManyField(User, related_name = 'seminars', through = UserSeminar)

class UserSeminar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seminar = models.ForeignKey(Seminar, on_delete=models.CASCADE)
    # rating = models.PositiveSmallIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # joined_at = models.DateTimeField(auto_now=True)
    # Seminar.sem.create_seminar()
    # Seminar.sem.all()

class ParticipantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , primary_key =True)

    university = models.CharField(max_length=50, null= True)
    accepted = models.BooleanField()      # bool

    seminars=models.ForeignKey( Seminar, null=True, related_name= 'participant', on_delete=models.SET_NULL)  # related_name

    # rating = models.PositiveSmallIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class InstructorProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)

    company = models.CharField(max_length=50, null=True)
    year = models.PositiveSmallIntegerField(null=True)   #  null?

    charge = models.ForeignKey( Seminar, null=True, related_name='instructor', on_delete=models.SET_NULL)  #  related_name

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
