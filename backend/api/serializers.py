from rest_framework import serializers
from .models import Patient, Doctors, Scan, Appointment, FamilyRelatives, Grouptable, MedicalHistory

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctors
        fields = '__all__'

class ScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scan
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

class FamilyRelativesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyRelatives
        fields = '__all__'

class GrouptableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grouptable
        fields = '__all__'

class MedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = '__all__'
