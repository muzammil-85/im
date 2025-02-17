from django.contrib import admin

from .models import Customer, CustomerItemPrice, CustomerOrder, Driver, Item, Payment, Receipt, Stock, Supplier, SupplierItemPrice, SupplierOrder

# Register your models here.
admin.site.register(Item)
admin.site.register(Stock)
admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(CustomerOrder)
admin.site.register(SupplierOrder)
admin.site.register(Driver)
admin.site.register(CustomerItemPrice)
admin.site.register(SupplierItemPrice)
admin.site.register(Receipt)
admin.site.register(Payment)

