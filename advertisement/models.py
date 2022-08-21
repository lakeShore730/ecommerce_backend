from django.db import models
from django.utils import timezone


class Advertisement(models.Model):
    image = models.ImageField(upload_to='advertisement')
    is_active =  models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(blank=True, null=True)


