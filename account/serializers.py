from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User, Role, Function



class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'slug',]

class FunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Function
        fields = ['id', 'name', 'description', 'slug',]



class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)  # Nested Role Serializer
    function = FunctionSerializer(read_only=True)  # Nested UserDetails Serializer
    
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'role', 'function', 'firstname', 'lastname', 'middlename', 'address', 'telephone', "is_active"]