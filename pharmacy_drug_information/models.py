from django.db import models

# Create your models here.
from enum import Enum
import datetime

class LogicEnum(Enum):
    AND = 'and'
    OR = 'or'
    NOT = 'not'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

class PharmacyDrugInformation(models.Model):
    generic_name  = models.CharField(max_length=100,null=False,unique=True)
    drug_efficasy_classification = models.CharField(max_length=100,null=False)
    effects = models.CharField(max_length=100)
    effects_logic = models.CharField(
        max_length=5,
        choices=LogicEnum.choices()
        # choices=[(tag,tag.value) for tag in LogicEnum]
    )
    warning = models.CharField(max_length=100)
    warning_logic =  models.CharField(
        max_length=5,
        choices=LogicEnum.choices()
        # choices=[(tag,tag.value) for tag in LogicEnum]
    )
    contraindications = models.CharField(max_length=100)
    contraindications_logic = models.CharField(
        max_length=5,
        choices=LogicEnum.choices()
        # choices=[(tag,tag.value) for tag in LogicEnum]
    )
    concomitant = models.CharField(max_length=100)
    concomitant_logic = models.CharField(
        max_length=5,
        choices=LogicEnum.choices()
        # choices=[(tag,tag.value) for tag in LogicEnum]
    ) 
    inquiry_company_name = models.CharField(max_length=100)
    start_update_date = models.DateField(auto_now_add=True)
    end_updated_date = models.DateField(auto_now=True) 
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True) 

