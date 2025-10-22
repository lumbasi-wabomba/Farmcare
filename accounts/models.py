from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustUser(AbstractUser):
    ROLES_CHOICES = [
        ('owner', 'Owner'),
        ('admin', 'Admin'),
        ('sales_clerk', 'Sales_clerk'),
    ]
    phone = models.CharField(max_length=15)
    role = models.CharField(max_length=50, default='sales_clerk', choices=ROLES_CHOICES)

    @property
    def IsAdminOrOwner(self):
        return self.role in ['owner', 'admin']
    
    @property
    def IsSalesClerOrAdmin(self):
        return self.role in ['sales_clerk', 'admin']

    def __str__(self):
        return f"{self.get_full_name()} : {self.role}"
    

class Salary(models.Model):
    user = models.ForeignKey(CustUser, on_delete=models.CASCADE, related_name='user_details')
    phone = models.CharField(max_length=15)
    date_joined = models.DateField(auto_now_add=True)
    amt_paid = models.DecimalField(max_digits=8, decimal_places=2)
    advance_payments = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    PAYMENT_METHOD_CHOICES = [
        ('Mpesa', 'mpesa'),
        ('Cash', 'cash'),
        ('Bank_transfer', 'bank_transfer')
    ]
    Payment_method = models.CharField(max_length=50, default='Mpesa', choices=PAYMENT_METHOD_CHOICES)

    def __str__(self):
        return f"{self.name} | {self.amt_paid} | {self.Payment_method}"
    


    
    



    
