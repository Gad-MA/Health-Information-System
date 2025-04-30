from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Patient, Doctors, Scan, Appointment, FamilyRelatives, Grouptable, MedicalHistory

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

    def create(self, validated_data):
        # Hash the password before saving
        raw_password = validated_data.pop('password', None)
        if raw_password:
            validated_data['password'] = make_password(raw_password)
        return super().create(validated_data)

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctors
        fields = '__all__'

    def create(self, validated_data):
        # Hash the password before saving
        raw_password = validated_data.pop('password', None)
        if raw_password:
            validated_data['password'] = make_password(raw_password)
        return super().create(validated_data)

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