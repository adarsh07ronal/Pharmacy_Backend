# Generated by Django 3.2.9 on 2022-07-10 14:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inquiry', '0003_inquiry_inquiry_pharmacist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inquiry',
            old_name='inquiry_pharmacist',
            new_name='inquiry_pharmacy',
        ),
    ]
