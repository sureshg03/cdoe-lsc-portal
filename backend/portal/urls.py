from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProgramViewSet, StudentViewSet, AttendanceViewSet,
    AssignmentMarkViewSet, CounsellorViewSet, ReportsViewSet
)

router = DefaultRouter()
router.register(r'programs', ProgramViewSet)
router.register(r'students', StudentViewSet)
router.register(r'attendance', AttendanceViewSet)
router.register(r'assignment-marks', AssignmentMarkViewSet)
router.register(r'counsellors', CounsellorViewSet)
router.register(r'reports', ReportsViewSet, basename='reports')

urlpatterns = [
    path('', include(router.urls)),
]