from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import VendorSerializer
from .models import Vendor
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.db import IntegrityError
from rest_framework.parsers import MultiPartParser, FormParser
# import pandas as pd
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, inline_serializer
from rest_framework import serializers

@extend_schema(
    tags=["vendors"],
    summary="Créer un fournisseur",
    description="Crée un nouveau fournisseur (Vendor) avec un `vendor_id` unique. Aucune authentification requise.",
    request={
        "application/json": {
            "type": "object",
            "required": ["vendor_id", "name"],
            "properties": {
                "vendor_id": {"type": "string", "example": "VEND-001"},
                "name": {"type": "string", "example": "Netis RDC"},
            },
            "additionalProperties": False,
        }
    },
    responses={
        201: OpenApiResponse(
            response=VendorSerializer,
            description="Fournisseur créé"
        ),
        400: OpenApiResponse(
            response=inline_serializer(
                name="VendorCreateError400",
                fields={"message": serializers.CharField()}  # <-- pas de example= ici
            ),
            description="Erreur de validation / unicité"
        ),
        500: OpenApiResponse(
            response=inline_serializer(
                name="VendorCreateError500",
                fields={"message": serializers.CharField()}  # <-- pas de example= ici
            ),
            description="Erreur interne"
        ),
    },
    examples=[
        OpenApiExample(
            "Exemple requête",
            value={"vendor_id": "VEND-001", "name": "Netis RDC"},
            request_only=True,
        ),
        OpenApiExample(
            "Exemple 201",
            value={"id": "uuid-ou-id", "vendor_id": "VEND-001", "name": "Netis RDC"},
            response_only=True,
        ),
        OpenApiExample(
            "Exemple 400",
            value={"message": "Ce vendor_id est déjà utilisé."},
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
def create_vendor(request):
    """
    Crée un nouveau fournisseur (Vendor) avec un vendor_id unique.
    """
    try:
        vendor_id = request.data.get('vendor_id')
        name = request.data.get('name')

        # Vérification si le vendor_id existe déjà
        if Vendor.objects.filter(vendor_id=vendor_id).exists():
            return JsonResponse({'message': 'Ce vendor_id est déjà utilisé.'}, status=status.HTTP_400_BAD_REQUEST)

        # Création du Vendor
        vendor = Vendor.objects.create(
            vendor_id=vendor_id,
            name=name,
        )

        serialized_vendor = VendorSerializer(vendor)
        return JsonResponse(serialized_vendor.data, status=status.HTTP_201_CREATED)

    except IntegrityError:
        return JsonResponse({'message': 'Erreur d\'unicité : Ce vendor_id existe déjà.'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return JsonResponse({'message': f'Erreur inattendue : {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    tags=["vendors"],
    summary="Lister tous les vendors",
    description="Retourne la **liste complète** des vendors (sans pagination).",
    responses={
        200: OpenApiResponse(
            response=VendorSerializer(many=True),
            description="Liste des vendors"
        ),
        500: OpenApiResponse(
            response=inline_serializer(
                name="VendorListServerError",
                fields={
                    "message": serializers.CharField(),
                    "error": serializers.CharField()
                }
            ),
            description="Erreur interne"
        ),
    },
    examples=[
        OpenApiExample(
            "Réponse 200 (exemple)",
            value=[
                {"id": "59a0f6f9-b6ec-4d5c-8a67-9f1e1d1b1c11", "name": "Global-Tech"},
                {"id": "3b4d0348-0c7c-4f18-9e0b-1b796b7b9d10", "name": "NOVACOM"}
            ],
            response_only=True,
        ),
        OpenApiExample(
            "Réponse 500 (exemple)",
            value={"message": "Internal server error", "error": "Detail de l'exception"},
            response_only=True,
        ),
    ],
)
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_all_vendor(request):
    try:
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
    except Exception as e:
        return JsonResponse({'message': 'Internal server error', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
