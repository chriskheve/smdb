from rest_framework import serializers
from .models import Sites
from vendor.serializers import VendorSerializer
from account.serializers import UserSerializer
from risk_assessment.serializers import RiskAssementSerializer

class SitesSerializer(serializers.ModelSerializer):
    risk_assessment = RiskAssementSerializer()
    vendor = VendorSerializer()
    zm = UserSerializer() 

    class Meta:
        model = Sites
        fields = [
            'id',
            'name',
            'site_id',
            'latitude',
            'longitude',
            'zm',
            'vendor',
            'security_type',
            'risk_assessment',
            'created_at'
        ]