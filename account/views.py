from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate

from .serializers import UserSerializer

# ⬇️ remplace ces imports drf_yasg :
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi

# ⬇️ par ceux de drf-spectacular :
from drf_spectacular.utils import (
    extend_schema, OpenApiExample, OpenApiResponse, inline_serializer
)
from rest_framework import serializers


class CustomLoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["auth"],
        summary="Login via email & password (JWT)",
        description="Authenticate user and return a JWT **access** and **refresh** token pair, plus user info.",
        request={
            "application/json": {
                "type": "object",
                "required": ["email", "password"],
                "properties": {
                    "email": {"type": "string", "format": "email", "description": "User email"},
                    "password": {"type": "string", "description": "User password"},
                },
                "additionalProperties": False,
            }
        },
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    name="LoginSuccess",
                    fields={
                        "token": inline_serializer(
                            name="TokenPair",
                            fields={
                                "refresh": serializers.CharField(help_text="Refresh token"),
                                "access": serializers.CharField(help_text="Access token"),
                            },
                        ),
                        "user": UserSerializer(),  # réutilise ton serializer existant
                    },
                ),
                description="Successful login",
                examples=[
                    OpenApiExample(
                        "Example 200",
                        value={
                            "token": {
                                "refresh": "eyJhbGciOiJIUzI1NiIsInR...",
                                "access": "eyJhbGciOiJIUzI1NiIsInR..."
                            },
                            "user": {
                                "id": "user-id-or-uuid",
                                "email": "user@example.com",
                                "name": "John Doe"
                            }
                        },
                        response_only=True,
                    )
                ],
            ),
            401: OpenApiResponse(
                response=inline_serializer(
                    name="LoginError",
                    fields={
                        "message": serializers.CharField(
                            default="Invalid email or password"
                        )
                    },
                ),
                description="Invalid email or password",
                examples=[
                    OpenApiExample(
                        "Example 401",
                        value={"message": "Invalid email or password"},
                        response_only=True,
                    )
                ],
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            user_data = UserSerializer(user).data

            return Response({
                'token': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                'user': user_data,
            }, status=status.HTTP_200_OK)

        return Response(
            {"message": "Invalid email or password"},
            status=status.HTTP_401_UNAUTHORIZED
        )
