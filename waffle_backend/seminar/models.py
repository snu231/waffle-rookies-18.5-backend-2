from django.contrib.auth.models import User

from django.db import models

# Create your models here.

class Seminar(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.PositiveSmallIntegerField()
    count = models.PositiveSmallIntegerField()
    time = models.TimeField()
    online = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    # sem = SeminarManager()
    # users = models.ManyToManyField(User, related_name = 'seminars', through = UserSeminar)

class UserSeminar(models.Model):
    PARTICIPANT = 'participant'
    INSTRUCTOR = 'instructor'

    ROLE_CHOICES = (

        (PARTICIPANT, PARTICIPANT),
        (PARTICIPANT, INSTRUCTOR)
    )

    ROLES = (PARTICIPANT, INSTRUCTOR)

    user = models.ForeignKey(User, related_name='user_seminars', on_delete=models.CASCADE)
    seminar = models.ForeignKey(Seminar, related_name='user_seminars', choices=ROLE_CHOICES, on_delete=models.CASCADE)
    dropped_at = models.DateTimeField(null=True)

    # rating = models.PositiveSmallIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, db_index=True)
    is_active = models.BooleanField(null=True) #
    # joined_at = models.DateTimeField(auto_now=True)
    # Seminar.sem.create_seminar()2
    # Seminar.sem.all()

    class Meta:
        unique_together = (
            ('user', 'seminar')
        )

class ParticipantProfile(models.Model):
    user = models.OneToOneField(User, related_name='participant' , on_delete=models.CASCADE, primary_key=True)

    university = models.CharField(max_length=50, null=True)
    accepted = models.BooleanField(null=True)      # bool

    seminars = models.ForeignKey(Seminar, null=True, related_name='participant', on_delete=models.SET_NULL)  # related_name

    # rating = models.PositiveSmallIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class InstructorProfile(models.Model):

    user = models.OneToOneField(User, related_name='instructor',on_delete=models.CASCADE, primary_key = True)

    company = models.CharField(max_length=50, null=True)
    year = models.PositiveSmallIntegerField(null=True)   #  null?

    charge = models.ForeignKey( Seminar, null=True, related_name='instructor', on_delete=models.SET_NULL)  #  related_name

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
