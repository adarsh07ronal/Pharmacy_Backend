# Generated by Django 3.2.9 on 2022-07-07 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PostingType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posting_type', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PublicationPlace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publication', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PharmaceuticalManufacturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listed_company_name', models.CharField(blank=True, max_length=30, null=True)),
                ('manager', models.CharField(max_length=30)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='email address')),
                ('telephone_number', models.CharField(max_length=500)),
                ('post_period_start', models.DateField(blank=True, null=True)),
                ('post_period_end', models.DateField(blank=True, null=True)),
                ('advertising_text', models.TextField(blank=True, null=True)),
                ('banner', models.FileField(blank=True, null=True, upload_to='manufacturer/banner/')),
                ('link_destination', models.CharField(blank=True, max_length=200, null=True)),
                ('no_of_exposures', models.IntegerField(default=0)),
                ('no_of_clicks', models.IntegerField(default=0)),
                ('no_of_cvs', models.IntegerField(default=0)),
                ('place_of_publication', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pharmaceutical_manufacturer.publicationplace')),
                ('posting_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pharmaceutical_manufacturer.postingtype')),
            ],
        ),
    ]
