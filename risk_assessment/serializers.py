from rest_framework import serializers
from .models import RiskAssessment

class RiskAssementSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskAssessment
        fields = ['id', 'name', 'created_at']  # Inclut tous les champs du modèle
        # read_only_fields = ['id', 'created_at']  # Rend ces champs non modifiables