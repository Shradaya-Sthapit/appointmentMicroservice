from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CreateAppointmentSerializer,ListAppointmentSerializer
from .models import Appointment
import jwt, datetime
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated,AllowAny
import datetime 
import requests
import json

class createAppointment(APIView):
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        headers = {"Authorization": token }
        patient = requests.get('http://localhost:8080/patient/validate',headers=headers)
        patientData=json.loads(patient.content)
        if 'code' in patientData.keys() and patientData['code'] =='token_not_valid':
            return Response(patientData)
        data=request.data
        doctorId=data['doctor']
        doctor = requests.get(f'http://localhost:8081/doctor/get/{doctorId}')
        doctorObj=json.loads(doctor.text)
        if datetime.datetime.strptime(data['startTime'], '%H:%M').time() < datetime.datetime.strptime(doctorObj['doctordetail']['inTime'],'%H:%M:%S').time() and datetime.datetime.strptime( data['endTime'], '%H:%M').time() > datetime.datetime.strptime(doctorObj['doctordetail']['outTime'],'%H:%M:%S').time():
            return Response("Selected Time out of range of doctors time")  
        appointment=Appointment.objects.filter(doctor=data['doctor'],startTime__lte=data['endTime'],endTime__gte=data['startTime'])  
        if len(appointment)>0:
            return Response("The appointment overlaps with existing appointments")
        
        serializer = CreateAppointmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class getDoctorAppointment(APIView):
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        headers = {"Authorization": token }
        doctor = requests.get('http://localhost:8081/doctor/validate',headers=headers)
        doctorData=json.loads(doctor.content)
        if 'code' in doctorData.keys() and doctorData['code'] =='token_not_valid':
            return Response(patientData)
        appointment = Appointment.objects.filter(doctor=doctorData['user_id'])
        serializer=ListAppointmentSerializer(appointment,many=True)
        return Response(serializer.data)

class getPatientAppointment(APIView):

    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        headers = {"Authorization": token }
        patient = requests.get('http://localhost:8080/patient/validate',headers=headers)
        patientData=json.loads(patient.content)
        if 'code' in patientData.keys() and patientData['code'] =='token_not_valid':
            return Response(patientData)
        appointment = Appointment.objects.filter(patient=patientData['user_id'])
        serializer=ListAppointmentSerializer(appointment,many=True)
        return Response(serializer.data)

class getAppointmentById(APIView):

    def get(self, request,id):
        appointment = Appointment.objects.get(id=id)
        serializer=ListAppointmentSerializer(appointment,many=False)
        return Response(serializer.data)

class updateAppointment(APIView):
    def patch(self, request,id):
        token = request.META.get('HTTP_AUTHORIZATION', " ")
        headers = {"Authorization": token }
        patient = requests.get('http://localhost:8080/patient/validate/',headers=headers)
        patientData=json.loads(patient.content)
        if 'code' in patientData.keys() and patientData['code'] =='token_not_valid':
            return Response(patientData)
        data=request.data
        doctorId=data['doctor']
        doctor = requests.get(f'http://localhost:8081/doctor/get/{doctorId}')
        doctorObj=json.loads(doctor.text)
        if datetime.datetime.strptime(data['startTime'], '%H:%M').time() < datetime.datetime.strptime(doctorObj['doctordetail']['inTime'],'%H:%M:%S').time() and datetime.datetime.strptime( data['endTime'], '%H:%M').time() > datetime.datetime.strptime(doctorObj['doctordetail']['outTime'],'%H:%M:%S').time():
            return Response("Selected Time out of range of doctors time")  
        appointment=Appointment.objects.filter(doctor=data['doctor'],startTime__lte=data['endTime'],endTime__gte=data['startTime']).exclude(id=id)
        if len(appointment)>0:
            return Response("The appointment overlaps with existing appointments")
        
        appointmentDetail =Appointment.objects.get(id=id)
        serializer=CreateAppointmentSerializer(instance=appointmentDetail,data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

class deleteAppointment(APIView):
    def delete(self, request,id):
        token = request.META.get('HTTP_AUTHORIZATION', " ")
        headers = {"Authorization": token }
        patient = requests.get('http://localhost:8080/patient/validate/',headers=headers)
        patientData=json.loads(patient.content)
        if 'code' in patientData.keys() and patientData['code'] =='token_not_valid':
            return Response(patientData)
        appointment = Appointment.objects.get(id=id)
        appointment.delete()
        return Response("Item Successfully Deleted")



    