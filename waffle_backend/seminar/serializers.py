from django.contrib.auth.models import User
from rest_framework import serializers
from seminar.models import ParticipantProfile, InstructorProfile, Seminar
from django.db import models

class SeminarSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True)

    class Meta:
        model =Seminar
        fields = (
            'id',   # seminar id
            'name',   # seminar name
            'dropped_out', #
            'joined_at',    #
        )

class ParticipantSerializer(serializers.ModelSerializer):

    seminars = serializers.SerializerMethodField()

    class Meta:
        model = ParticipantProfile  #
        fields = (
            'id',
            'university',
            'accepted',
            'seminars',  #
        )

    def get_seminars(self, seminar):
        if seminar.seminars :
            return SeminarSerializer(seminar.seminars, context=self.context).data
        return None

class InstructorSerializer(serializers.ModelSerializer):
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
    def get_charge(self, seminar):
        if seminar.charge :
            return SeminarSerializer(seminar.charge, context=self.context).data
        return None
