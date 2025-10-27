from .models import Products,PurchaseItems,Suppliers,Expense, Category
from rest_framework import serializers

class ProductsSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='category_name', many=False, required=False)
    class Meta:
        model = Products
        fields = '__all__'
        read_only_fields = ['category']

class PurchaseItemsSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(queryset=Products.objects.all(), slug_field='name', many=False, required=True)
    supplier = serializers.SlugRelatedField(queryset=Suppliers.objects.all(), slug_field='name', many=False, required=False)
    class Meta:
        model = PurchaseItems
        fields = '__all__'
        read_only_fields = ['product', 'supplier']

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields = '__all__'
    
class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'
        
