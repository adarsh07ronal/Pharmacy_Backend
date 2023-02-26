from rest_framework import serializers
from .models import PharmaceuticalManufacturer,PostingType,PublicationPlace
import humanize
from datetime import datetime, timezone

class PublicationPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model =PublicationPlace 
        fields = "__all__"

class PostingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model =PostingType
        fields = "__all__"

class PharmaceuticalManufacturerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model =PharmaceuticalManufacturer 
        fields = "__all__"

class PharmaceuticalManufacturerBannerNullSerializer(serializers.ModelSerializer):
    banner = serializers.FileField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
    class Meta:
        model =PharmaceuticalManufacturer 
        fields = "__all__"

class PharmaceuticalManufacturerSerializer(serializers.ModelSerializer):
    posting_type = PostingTypeSerializer()
    place_of_publication = PublicationPlaceSerializer()
    class Meta:
        model =PharmaceuticalManufacturer 
        fields = "__all__"

class AdvertisementDashboardSerializer(serializers.ModelSerializer):
    posting_status = serializers.SerializerMethodField('get_status_details')

    def get_status_details(self, obj, *args,**kwargs):
        current_date =  datetime.now().date()
        posting_date = obj.post_period_start
        gap = (current_date-posting_date)
        if gap.days >= 0:
            return "posted {}".format(humanize.naturaltime(gap))
        return "Waiting for publication start"
    
    class Meta:
        model =PharmaceuticalManufacturer 
        fields = ('listed_company_name','posting_status','post_period_start','post_period_end','no_of_exposures','no_of_clicks','no_of_cvs')