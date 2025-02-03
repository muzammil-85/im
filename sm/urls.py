from django.contrib import admin
from django.urls import path
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from stock.views import ItemViewSet, StockViewSet
from stock.views import export_stock_to_excel

router = DefaultRouter()
router.register(r'stocks', StockViewSet)
router.register(r'items', ItemViewSet, basename='item')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('export-stock/<str:date>/', export_stock_to_excel, name='export_stock'),
]
