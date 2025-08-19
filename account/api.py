from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from .serializers import RoleSerializer, UserSerializer

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .forms import SignupForm
from drf_spectacular.utils import (
    extend_schema, OpenApiExample, OpenApiResponse
)


@api_view(['GET'])
def me(request):
  user = request.user
  user_serializer = UserSerializer(user)
  return JsonResponse(user_serializer.data, safe=False)

@extend_schema(
    tags=["auth"],
    summary="Inscription d'un utilisateur",
    description=(
        "Crée un utilisateur **inactif** (en attente d'activation). "
        "Aucune authentification requise. "
        "Retourne `message: success` si OK, sinon un message d'erreur de validation."
    ),
    request={
        "application/json": {
            "type": "object",
            "required": ["email", "password1", "password2"],
            "properties": {
                "email": {"type": "string", "format": "email", "example": "alice@example.com"},
                "password1": {"type": "string", "example": "MonP@ssw0rd!"},
                "password2": {"type": "string", "example": "MonP@ssw0rd!"},
                "lastname": {"type": "string", "nullable": True, "example": "Doe"},
                "firstname": {"type": "string", "nullable": True, "example": "Alice"},
                "middlename": {"type": "string", "nullable": True},
                "address": {"type": "string", "nullable": True},
                "telephone": {"type": "string", "nullable": True, "example": "+243970000000"},
                "role_id": {"type": "string", "format": "uuid", "nullable": True},
                "function_id": {"type": "string", "format": "uuid", "nullable": True},
                "department_id": {"type": "string", "format": "uuid", "nullable": True},
                "vendor": {"type": "string", "nullable": True},
                "department": {"type": "string", "nullable": True}
            },
            "additionalProperties": False
        }
    },
    responses={
        200: {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "message": {"type": "string", "example": "success"}
                    },
                    "required": ["message"]
                }
            }
        },
        # Si tu gardes 500 pour la validation, documente comme ceci (sinon mets 400)
        400: {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "Message d'erreur concaténé (issu de form.errors)",
                            "example": "Email invalide Le mot de passe est trop court"
                        }
                    },
                    "required": ["message"]
                }
            }
        },
        500: {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "message": {"type": "string", "example": "Email invalide Le mot de passe est trop court"}
                    },
                    "required": ["message"]
                }
            }
        },
    },
    examples=[
        OpenApiExample(
            "Requête valide",
            value={
                "email": "alice@example.com",
                "password1": "MonP@ssw0rd!",
                "password2": "MonP@ssw0rd!",
                "firstname": "Alice",
                "lastname": "Doe",
                "telephone": "+243970000000",
                "role_id": "59a0f6f9-b6ec-4d5c-8a67-9f1e1d1b1c11",
                "function_id": "3b4d0348-0c7c-4f18-9e0b-1b796b7b9d10",
                "department_id": "c7b0c8b1-1c0e-4803-8d6e-3a1b799c9f22"
            },
            request_only=True,
        ),
        OpenApiExample(
            "Réponse succès",
            value={"message": "success"},
            response_only=True,
        ),
        OpenApiExample(
            "Réponse erreur",
            value={"message": "Les mots de passe ne correspondent pas"},
            response_only=True,
        ),
    ],
)

@api_view(['POST'])
@authentication_classes([])  # Désactive l'authentification pour cette vue
@permission_classes([])  # Accessible à tout le monde
def signup(request):
    data = request.data
    message = 'success'

    # Remplir le formulaire avec les données reçues
    form = SignupForm({
        'email': data.get('email'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
        'lastname': data.get('lastname'),
        'firstname': data.get('firstname'),
        'middlename': data.get('middlename'),
        'address': data.get('address'),
        'telephone': data.get('telephone'),
        'function': data.get('function'),
        'role': data.get('role'),
        'vendor': data.get('vendor'),
        'department': data.get('department'),
    })

    # Valider et sauvegarder le formulaire
    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False  # Désactiver l'utilisateur jusqu'à la vérification
        user.save()

        # Gérer les provinces (Many-to-Many)
        provinces_ids = data.get('provinces', [])
        if provinces_ids:
            user.provinces.set(provinces_ids)

        user.save()

        # Générer l'URL de vérification
        # activation_url = f"{settings.WEBSITE_URL}/activateemail/?email={user.email}&id={user.id}"

        # Envoyer un e-mail de vérification
        # send_mail(
        #     "Veuillez vérifier votre adresse email",
        #     f"Cliquez sur ce lien pour activer votre compte : {activation_url}",
        #     "noreply@example.com",
        #     [user.email],
        #     fail_silently=False,
        # )
    else:
        # Retourner les erreurs si le formulaire n'est pas valide
        error_messages = []
        for field, errors in form.errors.items():
            for error in errors:
                error_messages.append(error)  # Ajouter seulement le message d'erreur
        
        message = ' '.join(error_messages)  # Joindre les messages d'erreur
        # message = form.errors.as_json()
        return Response(
            {"message": message},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return JsonResponse({'message': message}, safe=False)

