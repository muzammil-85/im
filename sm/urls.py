from django.contrib import admin
from django.urls import path
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from stock.views import CashbookView, CustomerItemPriceViewSet, CustomerOrderViewSet, CustomerViewSet, DriverViewSet, ItemViewSet, LedgerView,\
PaymentViewSet, ReceiptViewSet, StockViewSet, SupplierItemPriceViewSet, SupplierOrderViewSet, SupplierViewSet
from stock.views import export_stock_to_excel

router = DefaultRouter()
router.register(r'stocks', StockViewSet)
router.register(r'items', ItemViewSet, basename='item')
router.register(r'customer', CustomerViewSet, basename='customer')
router.register(r'supplier', SupplierViewSet, basename='supplier')
router.register(r'customer-order', CustomerOrderViewSet, basename='customer-order')
router.register(r'supplier-order', SupplierOrderViewSet, basename='supplier-order')
router.register(r'driver', DriverViewSet, basename='driver')
router.register(r'customer-item-price', CustomerItemPriceViewSet, basename='customer-item-price')
router.register(r'supplier-item-price', SupplierItemPriceViewSet, basename='supplier-item-price')
router.register(r'receipt', ReceiptViewSet, basename='receipt')
router.register(r'payment', PaymentViewSet, basename='payment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/cashbook/', CashbookView.as_view(), name='cashbook-api'),
    path('api/ledger/', LedgerView.as_view(), name='ledger-api'),
    path('export-stock/<str:date>/', export_stock_to_excel, name='export_stock'),
]
