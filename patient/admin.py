from django.contrib import admin
# Register your models here.
from patient.models import PatientInsurance,Patient,Address,PatientDocument,Prescription,PrescriptionReceiptReservation

admin.site.register(Patient)
admin.site.register(PatientInsurance)
admin.site.register(Address)
admin.site.register(PatientDocument)
admin.site.register(Prescription)
admin.site.register(PrescriptionReceiptReservation)