from django.db import models

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=200, db_index=True)

    def __str__(self):
        return self.category_name
    
class Products(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='product_categories')
    unit_BP = models.DecimalField(max_digits=8, decimal_places=2)
    unit_SP = models.DecimalField(max_digits=8, decimal_places=2)
    no_of_Units = models.IntegerField()
    supplier = models.CharField(max_length=200, default='GENERAL_WHOLESALER')
    unit_profit = models.DecimalField(max_digits=8, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.unit_profit = (self.unit_SP - self.unit_BP)
        super().save(*args, **kwargs)

    def __str__(self):
        return f" name: {self.name} | category: {self.category} | number: {self.no_of_Units} | profit: {self.unit_profit}| BP: {self.unit_BP}"

class Suppliers(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} | {self.phone}"

class PurchaseItems(models.Model):
    product= models.ForeignKey(Products, on_delete=models.PROTECT, related_name='purchased_products')
    unit_BP = models.DecimalField(max_digits=8, decimal_places=2)
    no_of_Units = models.IntegerField()
    supplier = models.ForeignKey(Suppliers, on_delete=models.PROTECT, related_name='items_from_suppliers')
    date_bought = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.product:
            self.product,_ = Products.objects.get_or_create(
                name = self.product,
                unit_BP = self.unit_BP,
                unit_SP = (self.unit_BP + 25),
                no_of_Units = self.no_of_Units,
                Supplier = self.supplier

            )

        super().save(*args, **kwargs)
        self.product.no_of_Units += self.no_of_Units
        self.product.save()

    def __str__(self):
        return f"{self.product} | BP: {self.unit_BP} : | SP: {self.unit_SP}| NO: {self.no_of_Units}"

    

class Expense(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} | {self.amount} | {self.date}"
    