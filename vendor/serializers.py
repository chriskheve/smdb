from rest_framework import serializers
from .models import Vendor

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'name', 'vendor_id', 'created_at']  # Inclut tous les champs du modèle
        # read_only_fields = ['id', 'created_at']  # Rend ces champs non modifiables