# Generated by Django 4.1 on 2022-08-29 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('patient', models.IntegerField()),
                ('doctor', models.IntegerField()),
                ('date', models.DateField()),
                ('startTime', models.TimeField()),
                ('endTime', models.TimeField()),
                ('information', models.CharField(max_length=255)),
            ],
        ),
    ]