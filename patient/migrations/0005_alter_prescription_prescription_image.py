# Generated by Django 3.2.9 on 2022-07-14 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0004_rename_prescription_date_prescription_prescription_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescription',
            name='prescription_image',
            field=models.ImageField(blank=True, null=True, upload_to='patient/prescriptions/images'),
        ),
    ]