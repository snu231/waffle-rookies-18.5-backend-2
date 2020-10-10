from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from seminar.serializers import SeminarSerializer, ParticipantSerializer, InstructorSerializer

from seminar.models import Seminar, ParticipantProfile, InstructorProfile


class SeminarViewSet(viewsets.GenericViewSet):
    queryset = Seminar.objects.all()
    serializer_class = SeminarSerializer


class ParticipantViewSet(viewsets.GenericViewSet):
    queryset = ParticipantProfile.objects.all()
    serializer_class = ParticipantSerializer


class InstructorViewSet(viewsets.GenericViewSet):
    queryset = InstructorProfile.objects.all()
    serializer_class = InstructorSerializer


