from django.db import models


class Appointment(models.Model):
    id=models.AutoField(primary_key=True)
    patient = models.IntegerField()
    doctor = models.IntegerField()
    date = models.DateField()
    startTime = models.TimeField()
    endTime= models.TimeField()
    information=models.CharField(max_length=255)

