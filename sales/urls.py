from django.urls import path
from rest_framework import routers
from .views import SalesItemViewset, WeeklyReportView, MonthlyReportView

urlpatterns = [
    path('weekly_report/', WeeklyReportView.as_view(), name='weekly_report'),
    path('monthy_report/', MonthlyReportView.as_view(), name='monthly_report')
]

router = routers.DefaultRouter()
router.register(r'sales', SalesItemViewset, basename='sales')

urlpatterns += router.urls