from django.contrib import admin
from .models import Category, Products, PurchaseItems, Suppliers, Expense
# Register your models here.

admin.site.register(Category)
admin.site.register(Products)
admin.site.register(PurchaseItems)
admin.site.register(Suppliers)
admin.site.register(Expense)
