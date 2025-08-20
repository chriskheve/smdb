import uuid
from django.db import models
from account.models import User
from risk_assessment.models import RiskAssessment
from vendor.models import Vendor

# Create your models here.


class Sites(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(max_length=100, null=True)
  security_type = models.CharField(max_length=100, null=True)
  site_id = models.CharField(max_length=100, unique=True, null=True)
  latitude = models.CharField(max_length=100, null=True)
  longitude = models.CharField(max_length=100, null=True)
  vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, null=True
    )
  zm = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True
    )
  risk_assessment = models.ForeignKey(
        RiskAssessment, on_delete=models.CASCADE, null=True
    )
  
  created_at = models.DateTimeField(auto_now_add=True)
