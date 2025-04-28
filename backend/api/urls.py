from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('patients/', views.patients_list_create, name='patients_list_create'),
    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),

    path('doctors/', views.doctors_list_create, name='doctors_list_create'),
    path('doctors/<int:pk>/', views.doctor_detail, name='doctor_detail'),

    path('patients/<int:patient_id>/scans/', views.patient_scans, name='patient_scans'),
    path('patients/<int:patient_id>/appointments/', views.patient_appointments, name='patient_appointments'),
    path('doctors/<int:doctor_id>/appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('patients/<int:patient_id>/family/', views.patient_family, name='patient_family'),
    path('patients/<int:patient_id>/group/', views.patient_group, name='patient_group'),
    path('patients/<int:patient_id>/medical_history/', views.patient_medical_history, name='patient_medical_history'),
]
