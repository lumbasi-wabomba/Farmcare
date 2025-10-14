from .models import CustUser, Salary
from rest_framework import serializers


class CustUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustUser
        fields = '__all__'


class Salary(serializers.ModelSerializer):
    name = CustUser.get_full_name()
    user = serializers.SlugRelatedField(queryset=CustUser.objects.all(), slug_field=name, many=True)

    class Meta:
        model = Salary
        fields = '__all__'
        read_only_fields =['user']


