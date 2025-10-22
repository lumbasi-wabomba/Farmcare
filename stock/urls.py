from rest_framework import routers
from .views import PurchaseViewset, ProductViewset, ExpenseViewset

router = routers.DefaultRouter()
router.register(r'purchase', PurchaseViewset, basename='purchase')
router.register(r'products', ProductViewset, basename='products')
router.register(r'expense', ExpenseViewset, basename='expense')

urlpatterns = [
    
]
urlpatterns += router.urls