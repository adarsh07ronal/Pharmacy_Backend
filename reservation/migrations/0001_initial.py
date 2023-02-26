# Generated by Django 3.2.9 on 2022-07-07 11:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('patient', '0001_initial'),
        ('drugstore', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recieve_choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_en', models.CharField(blank=True, max_length=200, null=True)),
                ('choice_jpn', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserMemo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('memo_scheduled_time', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('pharmacy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='drugstore.drugstore')),
                ('prescription', models.ManyToManyField(blank=True, null=True, related_name='memos', to='patient.Prescription')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memo_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scheduled_time', models.DateTimeField(blank=True, null=True)),
                ('is_remote', models.BooleanField(default=False)),
                ('message', models.TextField()),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_reservation', to='patient.patient')),
                ('pharmacy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_reservation', to=settings.AUTH_USER_MODEL)),
                ('prescription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='presciption_reservation', to='patient.prescription')),
            ],
        ),
        migrations.CreateModel(
            name='ForReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_visted', models.BooleanField(blank=True, default=False, null=True)),
                ('is_accepted', models.BooleanField(blank=True, default=False, null=True)),
                ('is_remote_accepted', models.BooleanField(blank=True, default=False, null=True)),
                ('medication_guidence', models.BooleanField(blank=True, default=False, null=True)),
                ('remote_medication', models.CharField(blank=True, max_length=200, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('reservation_scheduled_time', models.DateTimeField(blank=True, null=True)),
                ('guidance_scheduled_time', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_for_reservation', to='patient.patient')),
                ('pharmacy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_for_reservation', to='drugstore.drugstore')),
                ('prescription', models.ManyToManyField(blank=True, null=True, related_name='reservations', to='patient.Prescription')),
                ('receive_prescription_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='reservation.recieve_choice')),
                ('scheduled_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservation_scheduler', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated_at'],
            },
        ),
    ]