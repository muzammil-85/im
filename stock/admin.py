from django.contrib import admin

from .models import Customer, CustomerOrder, Driver, Item, Stock, Supplier, SupplierOrder

# Register your models here.
admin.site.register(Item)
admin.site.register(Stock)
admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(CustomerOrder)
admin.site.register(SupplierOrder)
admin.site.register(Driver)