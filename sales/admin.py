from django.contrib import admin
from .models import SaleItems, SalesClerk, PaymentMethod

# Register your models here.
admin.site.register(SalesClerk)
admin.site.register(SaleItems)
admin.site.register(PaymentMethod)