from rest_framework import serializers
from .models import Program, Student, Attendance, AssignmentMark, Counsellor

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    program_name = serializers.CharField(source='program.name', read_only=True)
    counsellor_name = serializers.CharField(source='counsellor.counsellor_name', read_only=True)

    class Meta:
        model = Student
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    application_no = serializers.CharField(source='student.application_no', read_only=True)

    class Meta:
        model = Attendance
        fields = '__all__'

class AssignmentMarkSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    program_name = serializers.CharField(source='program.name', read_only=True)

    class Meta:
        model = AssignmentMark
        fields = '__all__'

class CounsellorSerializer(serializers.ModelSerializer):
    programme_assigned_name = serializers.CharField(source='programme_assigned.name', read_only=True)

    class Meta:
        model = Counsellor
        fields = '__all__'