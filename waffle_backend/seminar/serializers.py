from django.contrib.auth.models import User
from rest_framework import serializers
from seminar.models import ParticipantProfile, InstructorProfile, Seminar, UserSeminar
from django.db import models

class SeminarSerializer(serializers.ModelSerializer):
    time = serializers.TimeField(format='%H:%M')
    online = serializers.BooleanField(default=True)
    instructors = serializers.SerializerMethodField()
    participants = serializers.SerializerMethodField()

    class Meta:
        model = Seminar
        fields = (
            'id',   # seminar id
            'name',   # seminar name
            'capacity'
            'count',    #
            'time',
            'online',
            'instructors',
            'participants',

        )

    def get_instructors(self, seminar):
        instructor_seminars = seminar.user_seminars.filter(role=UserSeminar.INSTRUCTOR)
        return InstructorOfSeminarSerializer(instructor_seminars, many = True, context=self.context).data

    def get_participants(self, seminar):
        participant_seminars = seminar.user_seminars.filter(role=UserSeminar.PARTICIPANT)
        return ParticipantOfSeminarSerializer(participant_seminars, many=True, context=self.context).data

class InstructorOfSeminarSerializer(serializers.ModelSerializer):
    joined_at = serializers.DateTimeField(source='created_at')
    id = serializers.IntegerField(source='user.id')
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = UserSeminar
        fields = (
            'joined_at',
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
        )

class ParticipantOfSeminarSerializer(serializers.ModelSerializer):

    joined_at = serializers.DateTimeField(source='created_at')
    id = serializers.IntegerField(source='user.id')
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = UserSeminar
        fields = (
            'joined_at',
            'id',
            'username',
            'email',
            'first_name',
            'last_name',

            'is_active',
            'dropped_at',
        )


class ParticipantProfileSerializer(serializers.ModelSerializer):

    accepted = serializers.BooleanField(default=True, required=False)
    seminars = serializers.SerializerMethodField(read_only=True)

    user_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = ParticipantProfile  #
        fields = (
            'id',
            'university',
            'accepted',
            'seminars',  #
            'user_id',
        )

    def get_seminars(self, participant_profile):

        participant_seminars = participant_profile.user.user_seminars.filter(role=UserSeminar.PARTICIPANT)
        return SeminarASParticipantSerializer(participant_seminars, context=self.context).data


class InstructorProfileSerializer(serializers.ModelSerializer):
    #company = serializers.CharField(null=True)
    charge = serializers.SerializerMethodField()#
    # year = models.PositiveSmallIntegerField(null=True)
    class Meta:
        model = InstructorProfile
        fields = (
            'id',
            'company',
            'year',
            'charge',   #

        )
    def get_charge(self, instructor_profile):
        instructor_seminar = instructor_profile.user.user_seminars.filter(role=UserSeminar.INSTRUCTOR).last()
        if instructor_seminar :
            return SeminarASInstructorSerializer(instructor_seminar, context=self.context).data
        return None

class SeminarASParticipantSerializer(serializers.ModelSerializer):
    joined_at = serializers.DateTimeField(source='created_at')
    id = serializers.IntegerField(source='seminar.id')
    name = serializers.CharField(source='seminar.name')

    class Meta:
        model = UserSeminar
        fields = (
            'joined_at',
            'id',
            'name',
            'is_active',
            'dropped_at',
        )

class SeminarASInstructorSerializer(serializers.ModelSerializer):
    joined_at = serializers.DateTimeField(source='created_at')
    id = serializers.IntegerField(source='seminar.id')
    name = serializers.CharField(source='seminar.name')

    class Meta:
        model = UserSeminar
        fields = (
            'joined_at'
            'id'
            'name'
        )
