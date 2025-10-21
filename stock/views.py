from django.shortcuts import render
from rest_framework.decorators import action
from .models import Products, PurchaseItems, Expense
from .serializers import ProductsSerializer, PurchaseItemsSerializer, ExpenseSerializer
from rest_framework.authentication import TokenAuthentication
from accounts.permissions import IsAdminOrOwner, IsSalesClerkOrAdmin, IsAdmin
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.

class PurchaseViewset(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrOwner, IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PurchaseItems.objects.all()
    serializer_class = PurchaseItemsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fileds = ['date_bought']

    def get_queryset(self):
        date  = self.request.query_params.get('-date')
        if date:
            queryset = queryset.filter(date=date)
        return queryset
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data =request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save(sales_clerk=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(methods=['Patch'], detail=True, permission_classes=[IsAdmin])
    def partial_update(self, serializer, pk=None):
        purchase = self.get_object()
        if self.request.user != 'admin':
            raise PermissionDenied("you must be an admin to correct the code!")
        serializer = self.get_serializer(purchase, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

class ExpenseViewset(viewsets.ModelViewSet):
    permission_classes = [IsSalesClerkOrAdmin, IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()
    filterset_fields = ['date']
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        date = self.request.query_params.get('-date')
        if date:
            queryset = queryset.filter(date=date)
        return queryset
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data =request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save(sales_clerk=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def partial_update(self, serializer):
        expense = self.get_object()
        if self.request.user != 'admin':
            raise PermissionDenied("you must be an admin to correct the code!")
        serializer = self.get_serializer(expense, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def destroy(self, instance, pk=None):
        if self.request.user != 'admin':
            raise PermissionDenied("an admin is required!")
        instance.delete()

class ProductSeriaizerViewset(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrOwner, IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = ProductsSerializer
    queryset = Products.objects.all()



    

