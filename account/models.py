import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone
# from location.models import Province, SubRegion
# from vendor.models import Vendor
# from department.models import Department

# Create your models here.


class CustomUserManager(UserManager):
    def _create_user(self, name, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail address")
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_user(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(name, email, password, **extra_fields)
    
    def create_superuser(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(name, email, password, **extra_fields)

class Function(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=True, null=True, default='')
    description = models.CharField(max_length=255, blank=True, null=True, default='')
    slug = models.CharField(max_length=255, blank=True, null=True, default='')

class Role(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=True, null=True, default='')
    description = models.CharField(max_length=255, blank=True, null=True, default='')
    slug = models.CharField(max_length=255, blank=True, null=True, default='')

class Department(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=True, null=True, default='')
    description = models.CharField(max_length=255, blank=True, null=True, default='')
    slug = models.CharField(max_length=255, blank=True, null=True, default='')



class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=191)
    name = models.CharField(max_length=255, blank=True, default='')
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, null=True, blank=True
    )
    
    
    lastname = models.CharField(max_length=255, blank=True, null=True, default='')
    firstname = models.CharField(max_length=255, blank=True, null=True, default='')
    middlename = models.CharField(max_length=255, blank=True, null=True, default='')
    address = models.CharField(max_length=255, blank=True, null=True, default='')
    telephone = models.CharField(max_length=255, unique=True, blank=True, null=True)
    function = models.ForeignKey(
        Function, on_delete=models.CASCADE, null=True, blank=True
    )
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, null=True, blank=True
    )
    

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    