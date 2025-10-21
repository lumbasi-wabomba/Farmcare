from django.shortcuts import render
from .models import SaleItems,SalesClerk, PaymentMethod, Products
from accounts.permissions import IsAdmin,IsAdminOrOwner, IsSalesClerk, IsSalesClerkOrAdmin
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from .serializers import SaleItemsSerializer

# Create your views here.
class SalesItemViewset(viewsets.ModelViewSet):
    permission_classes = [IsSalesClerkOrAdmin, IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = SaleItemsSerializer
    queryset = SaleItems.objects.all().order_by('-date')
   
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
    
    @action(methods=['Patch'], detail=True, permission_classes=[IsAdmin])
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

