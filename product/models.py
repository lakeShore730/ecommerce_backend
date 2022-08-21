from django.db import models
from django.utils import timezone
from user.models import User

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    image = models.ImageField(upload_to='category_image', blank=True, null=True)
    is_active =  models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    
    def __str__(self):
        return self.name

 
class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    discount = models.FloatField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    description = models.TextField(max_length=1000)
    category = models.ManyToManyField(Category)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    is_active =  models.BooleanField(default=True)
    is_feature =  models.BooleanField(default=True)
    primary_image = models.ImageField(upload_to='product_image')
    secondary_image1 = models.ImageField(upload_to='product_image', blank=True, null=True)
    secondary_image2 = models.ImageField(upload_to='product_image', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
