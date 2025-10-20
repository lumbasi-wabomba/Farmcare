from django.shortcuts import render
from .models import SaleItems,SalesClerk, PaymentMethod, Products
from accounts.permissions import IsAdmin,IsAdminOrOwner, IsSalesClerk, IsSalesClerkOrAdmin
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate, get_user_model
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import PermissionDenied
from .serializers import SaleItemsSerializer, SalesClerkSerializer ,PaymentMethodSerializer

# Create your views here.
class