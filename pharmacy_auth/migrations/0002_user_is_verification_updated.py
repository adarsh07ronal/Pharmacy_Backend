# Generated by Django 3.2.9 on 2022-07-12 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_verification_updated',
            field=models.BooleanField(default=False),
        ),
    ]
