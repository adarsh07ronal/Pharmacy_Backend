# Generated by Django 3.2.9 on 2022-07-19 12:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0006_alter_patient_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='patientinsurance',
            options={'ordering': ['-updated_at']},
        ),
        migrations.AddField(
            model_name='patientinsurance',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patientinsurance',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
