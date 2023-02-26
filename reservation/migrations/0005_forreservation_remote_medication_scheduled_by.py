# Generated by Django 3.2.9 on 2022-07-14 04:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reservation', '0004_auto_20220713_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='forreservation',
            name='remote_medication_scheduled_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='guidance_scheduler', to=settings.AUTH_USER_MODEL),
        ),
    ]
