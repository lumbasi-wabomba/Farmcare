from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdmin, IsAdminOrOwner, IsOwner, IsSalesClerk

# Create your views here.
