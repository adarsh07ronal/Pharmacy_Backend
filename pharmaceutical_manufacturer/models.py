# Create your models here.
from __future__ import unicode_literals
from django.db import models

class PublicationPlace(models.Model):
    publication=models.CharField(max_length=200,null=True,blank=True)

class PostingType(models.Model):
    posting_type=models.CharField(max_length=200,null=True,blank=True)

class PharmaceuticalManufacturer(models.Model):
    listed_company_name = models.CharField(max_length=30,null=True,blank=True)
    manager = models.CharField(max_length=30)
    email = models.EmailField(null=True,blank=True,verbose_name="email address")
    telephone_number = models.CharField(max_length=500)
    post_period_start = models.DateField(null=True,blank=True)
    post_period_end = models.DateField(null=True,blank=True)
    publicationplace_choice = (
        ('Publication place A','Publication place A'),
        ('Publication place B','Publication place B'),
        ('Publication place C','Publication place C'),
    )
    place_of_publication = models.ForeignKey(PublicationPlace,null=True,blank=True,on_delete=models.SET_NULL)
    posting_choice = (
        ('text','text'),
        ('banner','banner'),
    )
    posting_type = models.ForeignKey(PostingType,null=True,blank=True,on_delete=models.SET_NULL)
    advertising_text =models.TextField(null=True, blank=True)
    banner =models.FileField(upload_to='manufacturer/banner/',null=True, blank=True)
    link_destination=models.CharField(max_length=200,null=True, blank=True)
    no_of_exposures = models.IntegerField(default=0)
    no_of_clicks =  models.IntegerField(default=0)
    no_of_cvs =  models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at',]