# Generated by Django 3.2.9 on 2022-07-18 05:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0005_alter_prescription_prescription_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='patient',
            options={'ordering': ['-created_at']},
        ),
    ]
