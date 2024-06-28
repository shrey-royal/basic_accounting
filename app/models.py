from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Homepage(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    contact_no = models.CharField(max_length=20, blank=True)
    organization_name = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    full_name = models.CharField(max_length=150, default='')  
    email = models.EmailField(max_length=254, unique=True)  # Ensure email field is unique

    # Add custom related names for groups and user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_permissions'
    )

    def __str__(self):
        return self.username
    


class Customer(models.Model):
    company_name = models.CharField(max_length=20, unique=True)
    owner_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    gstin = models.CharField(max_length=20, blank=True, null=True)


    def __str__(self):
        return self.company_name
    
class Quality(models.Model):
    quality_no = models.CharField(max_length=100)

    def __str__(self):
        return self.quality_no

class Point(models.Model):
    point = models.CharField(max_length=100)

    def __str__(self):
        return self.point

class Brand(models.Model):
    brand = models.CharField(max_length=100)

    def __str__(self):
        return self.brand


    
class SPage(models.Model):
    quality = models.ForeignKey('Quality', on_delete=models.CASCADE)
    point = models.ForeignKey('Point', on_delete=models.CASCADE)
    
    @property
    def quality_no(self):
        return self.quality.quality_no


class Lott(models.Model):
    lot_no = models.CharField(max_length=20)
    
    def __str__(self):
        return str(self.lot_no)
    


    
class Packing(models.Model):
    date_packing = models.DateField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=100)
    lot_no = models.CharField(max_length=100)
    quality = models.ForeignKey('Quality', on_delete=models.CASCADE)
    point = models.ForeignKey('Point', on_delete=models.CASCADE)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    lot_kgs = models.FloatField()
    total_weight = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


    def __str__(self):
        return f'{self.name} - {self.lot_no} ({self.quality}, {self.point}, {self.brand})'

class Bundle(models.Model):
    bundle_entry = models.ForeignKey(Packing, on_delete=models.CASCADE, related_name='bundles')
    bundle = models.CharField(max_length=100)
    grade = models.CharField(max_length=100)
    sizes = models.CharField(max_length=100)
    sheet = models.CharField(max_length=100)
    weight = models.CharField(max_length=100)
    remarks = models.CharField(max_length=200, blank=True, null=True)
    status = models.BooleanField(default=False)  # Field to track dispatch status
    bill_no = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f'{self.bundle} - {self.grade}'

class Selected(models.Model):
    packing = models.ForeignKey(Packing, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    bill_no = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f'{self.name} - {self.bill_no} ({self.date})'
    

class packing_slip_new(models.Model):
    bill_no = models.CharField(max_length=20, blank=True, null=True)
    vehicle_no = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f'{self.bill_no} - {self.vehicle_no}'