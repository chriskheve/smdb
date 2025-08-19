from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import RiskAssementSerializer
from .models import RiskAssessment
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.db import IntegrityError
from rest_framework.parsers import MultiPartParser, FormParser
# import pandas as pd
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, inline_serializer
from rest_framework import serializers

@extend_schema(
    tags=["Risk Assessment"],
    summary="Créer un assessment de risque",
    description="Crée un nouvel assessment . Aucune authentification requise.",
    request={
        "application/json": {
            "type": "object",
            "required": ["name"],
            "properties": {
                "name": {"type": "string", "example": "Red"},
            },
            "additionalProperties": False,
        }
    },
    responses={
        201: OpenApiResponse(
            response=RiskAssementSerializer,
            description="Assessment créé"
        ),
        400: OpenApiResponse(
            response=inline_serializer(
                name="RiskAssementCreateError400",
                fields={"message": serializers.CharField()}  # <-- pas de example= ici
            ),
            description="Erreur de validation / unicité"
        ),
        500: OpenApiResponse(
            response=inline_serializer(
                name="RiskAssementCreateError500",
                fields={"message": serializers.CharField()}  # <-- pas de example= ici
            ),
            description="Erreur interne"
        ),
    },
    examples=[
        OpenApiExample(
            "Exemple requête",
            value={"name": "Red"},
            request_only=True,
        ),
        OpenApiExample(
            "Exemple 201",
            value={"id": "uuid-ou-id", "name": "Red"},
            response_only=True,
        ),
        OpenApiExample(
            "Exemple 400",
            value={"message": "Ce name est déjà utilisé."},
            response_only=True,
        ),
        OpenApiExample(
            "Exemple 500",
            value={"message": "Erreur inattendue : ..."},
            response_only=True,
        ),
    ],
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def create_risk_assement(request):
    """
    Crée un nouvel assessment.
    """
    try:
        name = request.data.get('name')

        # Vérification si le risk existe déjà
        if RiskAssessment.objects.filter(name=name).exists():
            return JsonResponse({'message': 'Ce name est déjà utilisé.'}, status=status.HTTP_400_BAD_REQUEST)

        # Création du risk
        risk = RiskAssessment.objects.create(
            name=name,
        )

        serialized_risk = RiskAssementSerializer(risk)
        return JsonResponse(serialized_risk.data, status=status.HTTP_201_CREATED)

    except IntegrityError:
        return JsonResponse({'message': 'Erreur d\'unicité : Ce name existe déjà.'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return JsonResponse({'message': f'Erreur inattendue : {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
