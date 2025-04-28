from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Patient, Doctors, Scan, Appointment, FamilyRelatives, Grouptable, MedicalHistory
from .serializers import PatientSerializer, DoctorSerializer, ScanSerializer, AppointmentSerializer, FamilyRelativesSerializer, GrouptableSerializer, MedicalHistorySerializer




# login APIs

@api_view(['POST'])
def login(request):
    """
    POST { "email": "...", "password": "..." }
    """
    email    = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response(
            {"detail": "Email and password are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # First try patients:
    try:
        user = Patient.objects.get(email=email)
        role = 'patient'
    except Patient.DoesNotExist:
        # Then try doctors:
        try:
            user = Doctors.objects.get(email=email)
            role = 'doctor'
        except Doctors.DoesNotExist:
            return Response(
                {"detail": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED
            )

    # Now check password; assumes you’ve hashed passwords when saving:
    if not check_password(password, user.password):
        return Response(
            {"detail": "Invalid credentials."},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # If you reach here, authentication succeeded.
    if role == 'patient':
        serializer = PatientSerializer(user)
    else:
        serializer = DoctorSerializer(user)

    return Response({
        "role": role,
        "user": serializer.data
    }, status=status.HTTP_200_OK)






# Patient APIs

@api_view(['GET', 'POST'])
def patients_list_create(request):
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
    try:
        patient = Patient.objects.get(pk=pk)
    except Patient.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PatientSerializer(patient)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PatientSerializer(patient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        serializer = PatientSerializer(patient, data=request.data, partial=True)  # partial=True allows partial updates
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


@api_view(['GET', 'PUT', 'DELETE'])
def doctor_detail(request, pk):
    try:
        doctor = Doctors.objects.get(pk=pk)
    except Doctors.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DoctorSerializer(doctor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        doctor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Retrieve all scans for a patient
@api_view(['GET'])
def patient_scans(request, patient_id):
    scans = Scan.objects.filter(patient_id=patient_id)
    serializer = ScanSerializer(scans, many=True)
    return Response(serializer.data)


# Retrieve all appointments for a patient
@api_view(['GET'])
def patient_appointments(request, patient_id):
    appointments = Appointment.objects.filter(patient_id=patient_id)
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


# Retrieve all appointments for a doctor
@api_view(['GET'])
def doctor_appointments(request, doctor_id):
    appointments = Appointment.objects.filter(doctor_id=doctor_id)
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


# Retrieve family members for a patient
@api_view(['GET'])
def patient_family(request, patient_id):
    family = FamilyRelatives.objects.filter(patient_id=patient_id)
    serializer = FamilyRelativesSerializer(family, many=True)
    return Response(serializer.data)


# Retrieve group for a patient
@api_view(['GET'])
def patient_group(request, patient_id):
    group = Grouptable.objects.filter(patient_id=patient_id)
    serializer = GrouptableSerializer(group, many=True)
    return Response(serializer.data)


# Retrieve medical history for a patient
@api_view(['GET'])
def patient_medical_history(request, patient_id):
    history = MedicalHistory.objects.filter(patient_id=patient_id)
    serializer = MedicalHistorySerializer(history, many=True)
    return Response(serializer.data)
