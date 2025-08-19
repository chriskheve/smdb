import uuid
from django.db import models

# Create your models here.

class Vendor(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  vendor_id = models.CharField(max_length=100, blank=True, unique=True, null=True)
  name = models.CharField(max_length=100, blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)