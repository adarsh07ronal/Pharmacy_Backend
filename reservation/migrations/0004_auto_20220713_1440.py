# Generated by Django 3.2.9 on 2022-07-13 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0003_usermemo_is_usermemo_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='forreservation',
            name='is_seen_patient',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='forreservation',
            name='is_seen_pharmacy',
            field=models.BooleanField(default=True),
        ),
    ]