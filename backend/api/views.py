from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import (
    Patient, Doctors, Scan, Appointment, FamilyRelatives,
    Grouptable, MedicalHistory
)
from .serializers import (
    PatientSerializer, DoctorSerializer, ScanSerializer,
    AppointmentSerializer, FamilyRelativesSerializer,
    GrouptableSerializer, MedicalHistorySerializer
)


# Login API
@api_view(['POST'])
def login(request):
    """
    Handles user authentication for both patients and doctors.

    POST Request Body:
        {
            "email": "user@example.com",
            "password": "user_password"
        }

    Response:
        - On Success (HTTP 200):
            {
                "role": "patient" or "doctor",
                "user": {...}  # User details serialized
            }
        - On Error (HTTP 400 or 401):
            {
                "detail": "Error message"
            }
    """
    email = request.data.get('email')
    password = request.data.get('password')

    # Validate that email and password are provided
    if not email or not password:
        return Response(
            {"detail": "Email and password are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Try finding the user as a patient
        user = Patient.objects.get(email=email)
        role = 'patient'
    except Patient.DoesNotExist:
        try:
            # Try finding the user as a doctor
            user = Doctors.objects.get(email=email)
            role = 'doctor'
        except Doctors.DoesNotExist:
            return Response(
                {"detail": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED
            )

    # Validate the password
    if not check_password(password, user.password):
        return Response(
            {"detail": "Invalid credentials."},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # Serialize the user based on their role
    serializer = PatientSerializer(user) if role == 'patient' else DoctorSerializer(user)

    return Response(
        {
            "role": role,
            "user": serializer.data
        },
        status=status.HTTP_200_OK
    )


# Patient APIs
@api_view(['GET', 'POST'])
def patients_list_create(request):
    """
    Handles retrieving the list of patients or creating a new patient.
    """
    if request.method == 'GET':
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def patient_detail(request, pk):
    """
    Handles operations on an individual patient.
    """
    try:
        patient = Patient.objects.get(pk=pk)
    except Patient.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PatientSerializer(patient)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'  # Support partial updates
        serializer = PatientSerializer(patient, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        patient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Doctor APIs
@api_view(['GET', 'POST'])
def doctors_list_create(request):
    """
    Handles retrieving the list of doctors or creating a new doctor.
    """
    if request.method == 'GET':
        doctors = Doctors.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def doctor_detail(request, pk):
    """
    Handles operations on an individual doctor.
    """
    try:
        doctor = Doctors.objects.get(pk=pk)
    except Doctors.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'  # Support partial updates
        serializer = DoctorSerializer(doctor, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        doctor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Scan APIs
@api_view(['GET'])
def patient_scans(request, patient_id):
    """
    Retrieves all scans related to a specific patient.
    """
    scans = Scan.objects.filter(patient_id=patient_id)
    serializer = ScanSerializer(scans, many=True)
    return Response(serializer.data)


# Appointment APIs
@api_view(['GET'])
def patient_appointments(request, patient_id):
    """
    Retrieves all appointments related to a specific patient.
    """
    appointments = Appointment.objects.filter(patient_id=patient_id)
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def doctor_appointments(request, doctor_id):
    """
    Retrieves all appointments related to a specific doctor.
    """
    appointments = Appointment.objects.filter(doctor_id=doctor_id)
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


# Family APIs
@api_view(['GET'])
def patient_family(request, patient_id):
    """
    Retrieves all family relatives of a specific patient.
    """
    family = FamilyRelatives.objects.filter(patient_id=patient_id)
    serializer = FamilyRelativesSerializer(family, many=True)
    return Response(serializer.data)


# Group APIs
@api_view(['GET'])
def patient_group(request, patient_id):
    """
    Retrieves all group data for a specific patient.
    """
    group = Grouptable.objects.filter(patient_id=patient_id)
    serializer = GrouptableSerializer(group, many=True)
    return Response(serializer.data)


# Medical History APIs
@api_view(['GET'])
def patient_medical_history(request, patient_id):
    """
    Retrieves all medical history records for a specific patient.
    """
    history = MedicalHistory.objects.filter(patient_id=patient_id)
    serializer = MedicalHistorySerializer(history, many=True)
    return Response(serializer.data)