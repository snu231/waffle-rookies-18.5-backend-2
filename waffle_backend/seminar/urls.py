from django.urls import include, path
from rest_framework.routers import SimpleRouter
from seminar.views import

app_name = 'seminar'

router = SimpleRouter()
router.register('seminar',   , basename='seminar')  #

urlpatterns = [
    path('', include((router.urls))),
]


from django.urls import include, path
from rest_framework.routers import SimpleRouter
from survey.views import OperatingSystemViewSet, SurveyResultViewSet


router = SimpleRouter()
router.register('survey', SurveyResultViewSet, basename='survey')
router.register('os', OperatingSystemViewSet, basename='os')

urlpatterns = [
    path('', include((router.urls))),
]
