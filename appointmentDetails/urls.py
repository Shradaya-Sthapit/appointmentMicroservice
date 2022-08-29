from django.urls import path,include
from .views import createAppointment,getDoctorAppointment,getPatientAppointment,getAppointmentById,deleteAppointment,updateAppointment


urlpatterns = [

    path('create',  createAppointment.as_view()),
    path('get/doctor', getDoctorAppointment.as_view()),
    path('get/patient', getPatientAppointment.as_view()),
    path('get/<str:id>', getAppointmentById.as_view()),
    path('update/<str:id>', updateAppointment.as_view()),
    path('delete/<str:id>', deleteAppointment.as_view()),
]

