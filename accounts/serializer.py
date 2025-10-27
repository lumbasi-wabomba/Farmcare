from .models import CustUser, Salary
from rest_framework import serializers
from django.core.validators import RegexValidator

class CustUserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(validators=[RegexValidator(r'^\+?1?\d{9,15}$')])
    class Meta:
        model = CustUser
        fields = '__all__'
        #read_only_fields = []

class SalarySerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=CustUser.objects.all(), slug_field='name', many=False, required=False)
    phone = serializers.CharField(validators=[RegexValidator(r'^\+?1?\d{9,15}$')])
    class Meta:
        model = Salary
        fields = '__all__'
        read_only_fields = ['user']

        