from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Sum, Avg
from .models import Program, Student, Attendance, AssignmentMark, Counsellor
from .serializers import (
    ProgramSerializer, StudentSerializer, AttendanceSerializer,
    AssignmentMarkSerializer, CounsellorSerializer
)

class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [IsAuthenticated]

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def by_program(self, request):
        program_id = request.query_params.get('program_id')
        if program_id:
            students = self.queryset.filter(program_id=program_id)
            serializer = self.get_serializer(students, many=True)
            return Response(serializer.data)
        return Response({"error": "program_id required"}, status=400)

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

class AssignmentMarkViewSet(viewsets.ModelViewSet):
    queryset = AssignmentMark.objects.all()
    serializer_class = AssignmentMarkSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def by_program(self, request):
        program_id = request.query_params.get('program_id')
        if program_id:
            marks = self.queryset.filter(program_id=program_id)
            serializer = self.get_serializer(marks, many=True)
            return Response(serializer.data)
        return Response({"error": "program_id required"}, status=400)

class CounsellorViewSet(viewsets.ModelViewSet):
    queryset = Counsellor.objects.all()
    serializer_class = CounsellorSerializer
    permission_classes = [IsAuthenticated]

class ReportsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def summary(self, request):
        total_applications = Student.objects.count()
        confirmed_admissions = Student.objects.filter(admission_status='Confirmed').count()
        pending_payments = Student.objects.filter(payment_status='Pending').count()
        total_revenue = Student.objects.filter(payment_status='Paid').count() * 1000  # Assuming ₹1000 per student

        data = {
            'total_applications': total_applications,
            'confirmed_admissions': confirmed_admissions,
            'pending_payments': pending_payments,
            'revenue_generated': total_revenue,
        }
        return Response(data)

    @action(detail=False, methods=['get'])
    def application_report(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def unpaid_report(self, request):
        students = Student.objects.filter(payment_status='Pending')
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def confirmed_report(self, request):
        students = Student.objects.filter(admission_status='Confirmed')
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)