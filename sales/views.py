from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import SaleItems,SalesClerk, PaymentMethod, Products
from accounts.permissions import IsAdmin,IsAdminOrOwner, IsSalesClerk, IsSalesClerkOrAdmin
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import PermissionDenied
from .serializers import SaleItemsSerializer
from calendar import monthrange

# Create your views here.
class SalesItemViewset(viewsets.ModelViewSet):
    permission_classes = [IsSalesClerkOrAdmin, IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = SaleItemsSerializer
    queryset = SaleItems.objects.all()
   
    def get_queryset(self):
        date = self.request.query_params.get('date')
        if date:
            queryset = queryset.filter(date=date)
        return queryset
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data =request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save(sales_clerk=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def partial_update(self, serializer, pk=None):
        sale = self.get_object()
        if self.request.user != 'admin':
            raise PermissionDenied("you must be an admin to correct the code!")
        serializer = self.get_serializer(sale, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def destroy(self, instance, pk=None):
        if self.request.user != 'admin':
            raise PermissionDenied("an admin is required!")
        instance.delete()

@action(methods=['get'], detail=True)
class WeeklyReportView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrOwner, IsAuthenticated]
    queryset = SaleItems.objects.all().prefetch_related('sold_items', 'sales_by', 'sales_payment_method')
    serializer_class = SaleItemsSerializer

    def get_queryset(self):
        today = timezone.now().date()
        monday = today - timedelta(days=today.weekday())  
        saturday = monday + timedelta(days=5)

        data = SaleItems.objects.filter(date__range=[monday, saturday])
        serializer_data = list(data.values())
        return serializer_data
    
class MOnthlyReportView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrOwner, IsAuthenticated]
    queryset = SaleItems.objects.all().prefetch_related('sold_items', 'sales_by', 'sales_payment_method')
    serializer_class = SaleItemsSerializer

    def get_queryset(self):
        today = timezone.now().date()
        start_month = today.replace(day=1)
        end_month = today.replace(days=monthrange(today.year, today.month)[1])
        
        data = SaleItems.objects.filter(date__range=[start_month, end_month])
        serializer_data = list(data.values())
        return serializer_data
    


