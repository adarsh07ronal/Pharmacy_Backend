from django.db import models

# Create your models here.
# from enum import Enum

# class LogicEnum(Enum):
#     AND = 'and'
#     OR = 'or'
#     NOT = 'not'

#     @classmethod
#     def choices(cls):
#         return [(key.value, key.name) for key in cls]

class DrugEfficacyClassification(models.Model):
    drug_classification_en=models.CharField(max_length=200,null=True,blank=True) 
    drug_classification_jp=models.CharField(max_length=200,null=True,blank=True)

class PharmacyOTCInformation(models.Model):
    brand_name =models.CharField(max_length=200,null=True,blank=True)
    sales_name_code = models.CharField(max_length=200,null=True,blank=True)
    standard_name = models.CharField(max_length=500,null=True,blank=True)
    japan_standard_prod_classification_number = models.CharField(max_length=200,null=True,blank=True)
    yj_code = models.CharField(max_length=200,null=True,blank=True)
    medicinal_effect_classification_name =  models.CharField(max_length=200,null=True,blank=True)
    drug_classification =  models.ForeignKey(DrugEfficacyClassification,on_delete=models.SET_NULL,null=True,blank=True)
    approval_number =  models.CharField(max_length=200,null=True,blank=True)
    european_trademark_name =  models.CharField(max_length=200,null=True,blank=True)
    nhi_price_standard_listing_date =models.DateField(null=True,blank=True)
    sales_start_date =models.DateField(null=True,blank=True)
    saving_method = models.CharField(max_length=200,null=True,blank=True)
    expiration_date = models.CharField(max_length=200,null=True,blank=True)
    regulation_classification = models.CharField(max_length=500,null=True,blank=True)
    active_ingredient = models.CharField(max_length=500,null=True,blank=True)
    warning = models.CharField(max_length=500,null=True,blank=True)
    additive = models.CharField(max_length=500,null=True,blank=True)
    properties = models.TextField(null=True,blank=True)
    caveat = models.TextField(null=True,blank=True)
    contraindications = models.TextField(null=True,blank=True)
    contraindications_in_principle = models.TextField(null=True,blank=True)
    efficacy = models.TextField(null=True,blank=True)
    usage_dosage = models.TextField(null=True,blank=True)
    precautions_related_to_usage = models.TextField(null=True,blank=True)
    precautions_for_use = models.TextField(null=True,blank=True)
    important_basic_notes = models.TextField(null=True,blank=True)
    interaction = models.CharField(max_length=500,null=True,blank=True)
    drug_name = models.CharField(max_length=500,null=True,blank=True)
    clinical_symptoms = models.TextField(null=True,blank=True)
    mechanism_riskfactors = models.CharField(max_length=500,null=True,blank=True)
    caution_for_combined_use = models.TextField(null=True,blank=True)
    side_effects = models.TextField(null=True,blank=True)
    other_side_effects = models.TextField(null=True,blank=True)
    administration_to_the_elderly =models.TextField(null=True,blank=True)
    administration_to_pregnant_women =models.TextField(null=True,blank=True)
    administration_to_children =models.TextField(null=True,blank=True)
    overdose =models.TextField(null=True,blank=True)
    precautions_for_application =models.TextField(null=True,blank=True)
    pharmacokinetics = models.TextField(null=True,blank=True)
    pharmacology = models.CharField(max_length=500,null=True,blank=True)
    pharmacological_action = models.TextField(null=True,blank=True)
    physicochemical_knowledge_about_active_ingredients = models.TextField(null=True,blank=True)
    packaging = models.TextField(null=True,blank=True)
    main_documents_and_document_request_destinations= models.TextField(null=True,blank=True)
    document_request_destination = models.TextField(null=True,blank=True)
    information_on_medications_with_limited_dosing_periods = models.TextField(null=True,blank=True)
    name_of_manufacturer_or_distributor =models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

    def __str__(self):
        if self.brand_name and self.drug_name:
            return self.brand_name+"'s "+self.drug_name
        return str(self.id)

    class Meta:
        ordering = ['-updated_at']