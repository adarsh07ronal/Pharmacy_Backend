from django.db import models
from patient.models import Patient
from drugstore.models import DrugStore

# Create your models here.

# Can mark any DrugStore as patient's Favorite

class FavoriteDrugStore(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True,blank=True)
    drugstore = models.ForeignKey(DrugStore,on_delete=models.CASCADE,null=True,blank=True)
    is_favorite = models.BooleanField(default=0)
