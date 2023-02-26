from django.db import models

# Create your models here.
class MedicineTipsCategory(models.Model):
    type_name =  models.CharField(max_length=50,null=True,blank=True)
    # category_en = models.CharField(max_length=50,null=True,blank=True)
    category = models.CharField(max_length=50,null=True,blank=True)

# Medicine Tips for advising the user to follow for good health

class MedicineTips(models.Model):
    title = models.TextField(null=True,blank=True)
    tips_body = models.TextField(null=True,blank=True)
    category=models.ForeignKey(MedicineTipsCategory,on_delete=models.DO_NOTHING,null=True,blank=True,related_name="medicine_tips")
    image_registration=models.ImageField(upload_to='medicine_tips/registration',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Medicine Tips"
        verbose_name_plural = "Medicine Tips"
        ordering = ['-updated_at',]