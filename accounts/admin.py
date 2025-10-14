from django.contrib import admin
from .models import CustUser, Salary
# Register your models here.
admin.site.register(Salary)
admin.site.register(CustUser)