# Generated by Django 3.2.9 on 2022-07-07 11:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Slug', models.SlugField(unique=True)),
                ('slug_details', models.TextField(help_text='Detailed description of email when it send', max_length=500)),
                ('subject', models.CharField(max_length=200)),
                ('body', models.TextField()),
                ('delivery_type', models.CharField(choices=[('Immediate', 'Immediate'), ('Scheduled', 'Scheduled')], max_length=9)),
                ('deliver_time', models.TimeField(help_text='required if scheduled selected')),
                ('record_log', models.BooleanField(default=False)),
                ('pharmacy', models.BooleanField(default=False)),
                ('patient', models.BooleanField(default=False)),
                ('orthrus', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('message', models.TextField()),
                ('date_time', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('Unread', 'Unread'), ('Read', 'Read')], default='Unread', max_length=8)),
                ('date_read', models.DateField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'notifications',
                'verbose_name_plural': 'notifications',
            },
        ),
    ]
