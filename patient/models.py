from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from drugstore.models import DrugStore

User = get_user_model()


class Status(models.IntegerChoices):
    SELF = 1, _("Self")
    SPOUSE = 2, _("Spouse")
    DAUGHTER = 3, _('Daughter')
    SON = 4, _('Son')
    MOM = 5, _('Mom')
    DAD = 6, _('Dad')

class GenderChoice(models.TextChoices):
    MALE = 'male', _('Male')
    FEMALE = 'female', _('Female')


class InsuranceCardChoices(models.IntegerChoices):
    BUSINESS_CARD = 1, _("Business health insurance card")
    NATIONAL_CARD = 2, _("National health insurance card")

class IsActiveChoices(models.TextChoices):
    IN_USE = "in_use",_("In Use")
    STOPPING = "stopping", _("Stopping")

class Patient(models.Model):
    user = models.ForeignKey(User, null=True,blank=True,on_delete=models.CASCADE, related_name='patients')
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100,null=True,blank=True)
    dob = models.DateField(null=True,blank=True)
    phone_no = models.CharField(max_length=20,null=True,blank=True)
    email = models.CharField(max_length=200,unique=True)
    gender = models.CharField(max_length=50, choices=GenderChoice.choices, default=GenderChoice.MALE)
    allergy_info = models.TextField("Allergy information",null=True,blank=True)
    allergy_reactive = models.TextField("Allergic reactive drug",null=True,blank=True)
    type = models.IntegerField(
        choices=Status.choices,
        default=Status.SELF)
    comment = models.TextField(null=True,blank=True)
    pharmacy_visited = models.ManyToManyField(DrugStore,blank=True, related_name='pharmacy_patients')
    key_matter_information = models.TextField(null=True,blank=True)
    line_id = models.PositiveIntegerField(null=True,blank=True)
    is_active = models.CharField(max_length=15,choices=IsActiveChoices.choices,default=IsActiveChoices.IN_USE)
    is_linked = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at= models.DateTimeField(auto_now=True,null=True,blank=True)
    
    class Meta:
        ordering = ['-created_at',] 

class PatientInsurance(models.Model):
    patient = models.ForeignKey(Patient, null=True,blank=True, on_delete=models.CASCADE, related_name='patient_insurance')
    card_choices = models.IntegerField(choices=InsuranceCardChoices.choices,null=True,blank=True)
    card_image = models.ImageField(upload_to='insurance',null=True,blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    date_of_issuance = models.DateField(null=True, blank=True)
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date_of_qualification = models.DateField(null=True, blank=True)
    name_of_head_of_household= models.CharField(max_length=30, null=True, blank=True)
    office_name = models.CharField(max_length=30, null=True, blank=True)
    insurance_number = models.CharField(max_length=100)
    recipient_name = models.CharField(max_length=30, null=True, blank=True)
    insurer_name = models.CharField(max_length=50, null=True, blank=True)
    insurer_location = models.CharField(max_length=20, null=True, blank=True)
    underlying_disease = models.TextField(null=True, blank=True)
    family_medical_institution = models.CharField(max_length=30, null=True, blank=True)
    family_dispensing_pharmacy = models.CharField(max_length=30, null=True, blank=True)
    pharmacist_in_charge = models.CharField(max_length=30, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.patient} - {self.get_card_choices_display()}'
    
    class Meta:
        ordering = ['-updated_at',] 


class Address(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='address')
    address = models.CharField(max_length=2000,null=True,blank=True)
    city = models.CharField(max_length=20)
    prefecture = models.CharField(max_length=50,null=True,blank=True)
    telephone = models.CharField(max_length=20,null=True,blank=True)

    def __str__(self):
        if self.address:
            return self.address


class PatientDocument(models.Model):
    employee = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='documents')
    name = models.CharField(max_length=100)
    date = models.DateField()
    text = models.TextField(max_length=20)
    file = models.FileField(upload_to='patient/document/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class GenericDrugsChoice(models.TextChoices):
    POSSIBLE = 'possible', _('possible')
    IMPOSSIBLE = 'impossible', _('impossible')

class SplitDispensingChoice(models.IntegerChoices):
    ONE = 1, ('1')
    TWO = 2, ('2')
    THREE = 3, ('3')
    FOUR = 4, ('4')
    FIVE = 5, ('5')
    SIX = 6, ('6')
    SEVEN = 7, ('7')
    EIGHT = 8, ('8')
    NINE = 9, ('9')
    TEN = 10, ('10')


class Prescription(models.Model):
    patient = models.ForeignKey(Patient,null=True,blank=True, on_delete=models.CASCADE, related_name='prescription')
    prescription_date  = models.DateField(max_length=4)
    time = models.TimeField(null=True,blank=True)
    isRed = models.BooleanField(default=False)
    insurer_number = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    birthday = models.DateField(max_length=4)
    gender = models.CharField(max_length=50, choices=GenderChoice.choices, default=GenderChoice.MALE)
    medical_institution_name = models.CharField(max_length=50)
    contact = models.CharField(max_length=20)
    prescribing_physician = models.CharField(max_length=50)
    prescription_details = models.TextField()
    change_to_generic_drugs = models.CharField(max_length=50, choices=GenericDrugsChoice.choices, default=GenericDrugsChoice.POSSIBLE)
    number_of_split_dispensing = models.IntegerField(choices=SplitDispensingChoice.choices, default=SplitDispensingChoice.ONE)
    prescription_image = models.ImageField(upload_to='patient/prescriptions/images',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at',]

class PrescriptionReceiptReservation(models.Model):
    date = models.DateField(null=True,blank=True)
    time = models.TimeField(null=True,blank=True)
    prescription = models.ForeignKey(Prescription,on_delete=models.CASCADE,related_name='reservation')
    is_remote = models.BooleanField(default=False)
    message = models.TextField()

class FilterCategory(models.Model):
    category_id = models.IntegerField(unique=True)
    filter_category_en = models.CharField(max_length=200,null=True,blank=True)
    filter_category_jpn = models.CharField(max_length=200,null=True,blank=True)
