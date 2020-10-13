from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from seminar.serializers import SeminarSerializer, ParticipantProfileSerializer, InstructorProfileSerializer

from seminar.models import Seminar, ParticipantProfile, InstructorProfile, UserSeminar
from seminar.permissions import IsParticipant, IsInstructor

class SeminarViewSet(viewsets.GenericViewSet):
    queryset = Seminar.objects.all()
    serializer_class = SeminarSerializer
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.action in ('create', 'update'):
            return (IsInstructor(), )
        elif self.action == 'user' and self.request.method == 'DELETE':
            return (IsParticipant(), )
        return super(SeminarViewSet, self).get_permissions()

    def get_serializer_class(self):
        if self.action == 'list':
            return self.serializer_class

    def create(self, request):
        user = request.user

        if user.user_seimnars.filter(role = 'instructor').exist():
            return Response({"error: another seminar"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        seminar = serializer.save()

        UserSeminar.objects.create(user=user, seminar=seminar, role=UserSeminar.INSTRUCTOR)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        user = request.user
        seminar = self.get_object()

        if not user.user_seminars.filter(seminar=seminar, role='instructor').exist():
            return Response({"error. not in charge of this sem"}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        serializer = self.get_serializer(seminar, data=data, partial= True)
        serializer.is_valid(raise_exception=True)

        participant_count = seminar.user_seminars.filter(role=UserSeminar.PARTICIPANT, is_active=True).count()
        if data.get('capacity') and int(data.get('capacity')) < participant_count:
            return Response({"error. capacipty must be more than num of participants"}, status=status.HTTP_400_BAD_REQUEST)

        serializer.update(seminar, serializer.validated_data)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        seminar = self.get_object()
        return Response(self.get_serializer(seminar).data)

    def list(self, request):

        name = request.query_params.get('name')
        order = request.query_params.get('order')

        seminars = self.get_queryset()

        if name:
            seminars = seminars.filter(name__icontains=name)
        if order == 'earliest':
            seminars = seminars.order_by('-created_at')
        return Response(self.get_serializer(seminars, many=True).data)

    def user(self, request, pk):
        seminar = self.get_object()

        if self.request.method == 'POST':
            return self._join_seminar(seminar)
        elif self.request.method == 'DELETE':
            return self._drop_seminar(seminar)

    def _join_seminar(self, seminar):
        user = self.request.user()
        role = self.request.data.get('role')

        if role not in UserSeminar.ROLES:
            return Response({"error. not participant or instructor"}, status=status.HTTP_400_BAD_REQUEST)

        if user.user_seminars.filter(seminar=seminar).exist():
            return Response({"error. have already joined the sem"}, status=status.HTTP_400_BAD_REQUEST)

        if role == UserSeminar.PARTICIPANT:
            if not hasattr(user, 'participant'):
                return Response({"error. not participant"}, status = status.HTTP_403_FORBIDDEN)
            if not user.participant.accepted:
                return Response({"error. not accepted"}, status=status.HTTP_403_FORBIDDEN)

            with transaction.atomic():
                participant_count = seminar.user_seminars.select_for_update().filter(
                    role=UserSeminar.PARTICIPANT, is_active=True).count()

                if participant_count >= seminar.capacity:
                    return Response("{error. already full}", status=status.HTTP_400_BAD_REQUEST)

                UserSeminar.objects.create(user=user, seminar = seminar, role=UserSeminar.PARTICIPANT)

        else:
            if not hasattr(user, 'instructor'):
                return Response({"error. not instructor"}, status=status.HTTP_403_FORBIDDEN)
            if user.user_seminars.filter(role = UserSeminar.INSTRUCTOR.exist()):
                return Response({"error. charge of another seminar"}, status=status.HTTP_400_BAD_REQUEST)

            UserSeminar.objects.create(user=user, seminar= seminar, role=UserSeminar.INSTRUCTOR)

    def _drop_seminar(self, seminar):
        user = self.request.user

        user_seminar = user.user_seminars.filter(seminar=seminar).last()

        if user_seminar and user_seminar.is_active:
            user_seminar.dropped_at = timezone.now()
            user_seminar.is_active = False
            user_seminar.save()

        seminar.refresh_from_db()

        return Response(self.get_serializer(seminar).data)

class ParticipantViewSet(viewsets.GenericViewSet):
    queryset = ParticipantProfile.objects.all()
    serializer_class = ParticipantProfileSerializer


class InstructorViewSet(viewsets.GenericViewSet):
    queryset = InstructorProfile.objects.all()
    serializer_class = InstructorProfileSerializer


