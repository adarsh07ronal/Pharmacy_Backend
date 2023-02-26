from __future__ import unicode_literals
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField

User = get_user_model()

# Prefecture Information. Moreover like districts

class Prefecture(models.Model):
    prefecture_rank = models.PositiveIntegerField(null=True,blank=True)
    prefecture_name_en=models.CharField(max_length=200,null=True,blank=True) 
    prefecture_name_jp=models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.prefecture_name_en +" "+self.prefecture_name_jp

    class Meta:
        ordering = ['prefecture_rank',]

# DrugStore/ Pharmacy information

class DrugStore(models.Model):
    prefecture_choices = (('北海道','北海道'),('青森県','青森県'),('岩手県','岩手県'),('宮城県','宮城県'),('秋田県','秋田県'),('山形県','山形県'),('福島県','福島県'),('茨城県','茨城県'),('栃木県','栃木県'),("\'群馬県","\'群馬県"),('埼玉県','埼玉県'),('千葉県','千葉県'),('東京都','東京都'),('神奈川県','神奈川県'),('新潟県','新潟県'),('富山県','富山県'),('石川県','石川県'),('福井県','福井県'),('山梨県','山梨県'),('長野県','長野県'),('岐阜県','岐阜県'),('静岡県','静岡県'),('愛知県','愛知県'),('三重県','三重県'),('滋賀県','滋賀県'),("\'京都府大阪府","\'京都府大阪府"),("兵庫県","兵庫県"),("奈良県","奈良県"),("和歌山県","和歌山県"),("鳥取県","鳥取県"),("島根県","島根県"),("岡山県","岡山県"),("広島県","広島県"),("山口県","山口県"),("徳島県","徳島県"),("香川県","香川県"),("愛媛県","愛媛県"),("高知県","高知県"),("福岡県","福岡県"),("佐賀県","佐賀県"),("長崎県","長崎県"),("熊本県","熊本県"),("大分県","大分県"),("宮崎県","宮崎県"),("鹿児島県","鹿児島県"),("沖縄県","沖縄県"))
    class_choices =(('prescription','prescription'),('first drug','first drug'),('second drug','second drug'),('daily necessities','daily necessities'),('food','food'))
    prefectures = models.ForeignKey(Prefecture,null=True,blank=True,on_delete=models.SET_NULL)
    # models.CharField(max_length=200,null=True,blank=True,choices=prefecture_choices)
    user = models.ForeignKey(User,blank=True,null=True,related_name="drugstore_user",on_delete=models.CASCADE,unique=True)
    drugstore_name = models.CharField(max_length=200,null=True,blank=True)
    # drugstore_type = models.CharField(max_length=200,null=True,blank=True)
    # classification = models.CharField(max_length=200,null=True,blank=True,choices=class_choices)
    handling_classification = ArrayField(models.CharField(max_length=200,choices=class_choices), blank=True,null=True)
    address = models.CharField(max_length=1000)
    postal_code = models.CharField(max_length=100,null=True,blank=True)
    municipalities = models.CharField(max_length=100,null=True,blank=True)
    fax = models.CharField(max_length=500,blank=True,null=True)
    email = models.EmailField('email address',null=True,blank=True,unique=True)
    is_linked = models.BooleanField(default=False)
    business_hours = models.CharField(max_length=500,null=True,blank=True)
    established =models.DateTimeField(null=True,blank=True) 
    time1_start=models.TimeField(null=True,blank=True) 
    time1_end=models.TimeField(null=True,blank=True) 
    time2_start=models.TimeField(null=True,blank=True) 
    time2_end=models.TimeField(null=True,blank=True) 
    telephone_number = models.CharField(max_length=500)
    representative = models.CharField(max_length=500,null=True,blank=True)
    # models.ForeignKey(User,related_name="Representative",on_delete=models.CASCADE,null=True,blank=True)
    no_of_employee =models.IntegerField(null=True,blank=True)
    line_id = models.PositiveIntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at',]