from .models import SaleItems, SalesClerk, PaymentMethod
from accounts.models import CustUser
from stock.models import Products
from rest_framework import serializers


class SalesClerkSerializer(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(queryset=CustUser.objects.all(), slug_field='name', many=False, required=True)
    class Meta:
        model = SalesClerk
        fields = '__all__'
        read_only_fields = ['name']

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'

class SaleItemsSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(queryset=Products.objects.all(), slug_field='name', many=False, required=True)
    sales_clerk = serializers.SlugRelatedField(queryset=SalesClerk.objects.all(), slug_field='name', many=False, required=False)
    class Meta:
        model = SaleItems
        fields = '__all__'
        read_only_fields = ['product', 'sales_clerk']


