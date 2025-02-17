from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from stock.views import (
    ItemViewSet, LoginAPI, StockViewSet, CustomerViewSet, SupplierViewSet, CustomerOrderViewSet,
    SupplierOrderViewSet, DriverViewSet, CustomerItemPriceViewSet, SupplierItemPriceViewSet,
    ReceiptViewSet, PaymentViewSet, CashbookView, LedgerView, export_stock_to_excel
)

# Create a router and register all ViewSets
router = DefaultRouter()

# Item URLs
router.register(r'items', ItemViewSet, basename='item')

# Stock URLs
router.register(r'stocks', StockViewSet, basename='stock')

# Customer URLs
router.register(r'customers', CustomerViewSet, basename='customer')

# Supplier URLs
router.register(r'suppliers', SupplierViewSet, basename='supplier')

# CustomerOrder URLs
router.register(r'customer-orders', CustomerOrderViewSet, basename='customer-order')

# SupplierOrder URLs
router.register(r'supplier-orders', SupplierOrderViewSet, basename='supplier-order')

# Driver URLs
router.register(r'drivers', DriverViewSet, basename='driver')

# CustomerItemPrice URLs
router.register(r'customer-item-prices', CustomerItemPriceViewSet, basename='customer-item-price')

# SupplierItemPrice URLs
router.register(r'supplier-item-prices', SupplierItemPriceViewSet, basename='supplier-item-price')

# Receipt URLs
router.register(r'receipts', ReceiptViewSet, basename='receipt')

# Payment URLs
router.register(r'payments', PaymentViewSet, basename='payment')


# Custom URLs for additional views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/login/', LoginAPI.as_view(), name='login'), 
    path('api/cashbook/', CashbookView.as_view(), name='cashbook-api'),
    path('api/ledger/', LedgerView.as_view(), name='ledger-api'),
    path('export-stock/<str:date>/', export_stock_to_excel, name='export_stock'),
]