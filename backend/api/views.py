import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection

@csrf_exempt
def patient_list(request):
    """
    List all patients or create a new patient
    """
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, name FROM patient ORDER BY id")
            rows = cursor.fetchall()
            
            patients = []
            for row in rows:
                patients.append({
                    'id': row[0],
                    'name': row[1]
                })
            
            return JsonResponse({'patients': patients})
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            
            if not name:
                return JsonResponse({'error': 'Name is required'}, status=400)
            
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO patient (name) VALUES (%s) RETURNING id", [name])
                patient_id = cursor.fetchone()[0]
            
            return JsonResponse({'id': patient_id, 'name': name}, status=201)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def patient_detail(request, patient_id):
    """
    Retrieve, update or delete a patient
    """
    # Check if patient exists
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, name FROM patient WHERE id = %s", [patient_id])
        patient = cursor.fetchone()
    
    if not patient:
        return JsonResponse({'error': 'Patient not found'}, status=404)
    
    if request.method == 'GET':
        return JsonResponse({
            'id': patient[0],
            'name': patient[1]
        })
    
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            
            if not name:
                return JsonResponse({'error': 'Name is required'}, status=400)
            
            with connection.cursor() as cursor:
                cursor.execute("UPDATE patient SET name = %s WHERE id = %s", [name, patient_id])
            
            return JsonResponse({'id': patient_id, 'name': name})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    elif request.method == 'DELETE':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM patient WHERE id = %s", [patient_id])
        
        return JsonResponse({'message': f'Patient {patient_id} deleted successfully'})
    
    return JsonResponse({'error': 'Invalid method'}, status=405)