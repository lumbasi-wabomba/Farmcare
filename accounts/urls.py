from django.urls import path
from rest_framework import routers
from django.contrib import admin
from .views import RegisterClerkView, LoginView, LogoutView, ProfileViewset, SalaryViewset

urlpatterns =[
    path('register_clerk/', RegisterClerkView.as_view(), name='register_clerk'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login')

]

router = routers.DefaultRouter()
router.register(r'profile', ProfileViewset, basename='profile')
router.register(r'salary', SalaryViewset, basename='salary')

urlpatterns += router.urls