from django.db import models
from stock.models import Products
from accounts.models import CustUser

# Create your models here.
class SalesClerk(models.Model):
    name = models.ForeignKey(CustUser, on_delete=models.CASCADE, related_name='clerk_details')
    check_in = models.DateTimeField(auto_now_add=True)
    check_out = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class PaymentMethod(models.Model):
    PAYMENT_METHOD_CHOICES= [
        ('Mpesa', 'mpesa'),
        ('Cash', 'cash'),
        ('Credit', 'credit')
    ]
    payment_method = models.CharField(max_length=50,choices=PAYMENT_METHOD_CHOICES)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    mpesa_code = models.CharField(max_length=50, blank=True, null=True)



class SaleItems(models.Model):
    cust_name = models.CharField(max_length=100, blank=True, null=True)
    product = models.ForeignKey(Products, on_delete=models.DO_NOTHING, related_name='sold_items')
    quantity = models.PositiveIntegerField()
    selling_price = models.DecimalField(max_digits=8, decimal_places=2, editable=False)
    profit = models.DecimalField(max_digits=8, decimal_places=2, editable=False)
    total = models.DecimalField(max_digits=8, decimal_places=2, editable=False)
    sales_clerk = models.ForeignKey(SalesClerk, on_delete=models.DO_NOTHING, related_name='sales_by')
    date = models.DateField(auto_created=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.DO_NOTHING, related_name='sales_payment_type')

    def update_totals(self):
        items = self.items.all()
        self.total_amount = sum(i.total for i in items)
        self.total_profit = sum(i.profit for i in items)
        self.save()

    def save(self, *args, **kwargs):
        self.selling_price = self.product.unit_SP
        self.buying_price = self.product.unit_BP
        self.profit = (self.selling_price - self.buying_price) * self.quantity
        self.total = self.selling_price * self.quantity
        super().save(*args, **kwargs)

        if self.product.no_of_Units >= self.quantity:
            self.product.no_of_Units -= self.quantity
        else:
            self.quantity = self.product.no_of_Units
            self.product.no_of_Units = 0
            
        self.product.save()

    def __str__(self):
        return f" item: {self.product} | quantity {self.quantity}"
    
