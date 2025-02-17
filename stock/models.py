from django.db.models import Sum
from django.db import models, transaction
from django.contrib.auth.models import User
class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    piece_per_box = models.IntegerField(default=0)
    mrp = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'item'

class Stock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='stock_entries')
    date = models.DateField()  # The day when the stock is recorded
    item_date = models.DateField()  # Specific item's date
    time = models.TimeField(auto_created=True,auto_now=True)
    total_qty = models.IntegerField(editable=False)

    def __str__(self):
        return  str(self.date)+' '+self.item.name
    class Meta:
        db_table = 'stock'

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    shopname = models.CharField(max_length=100, blank=True, null=True)  # Optional field
    phone_no = models.CharField(max_length=15)
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class Supplier(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    shopname = models.CharField(max_length=100, blank=True, null=True)  # Optional field
    phone_no = models.CharField(max_length=15)
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class Driver(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    vehicle_name = models.CharField(max_length=100, blank=True, null=True)  # Optional field
    vehicle_no = models.CharField(max_length=50)
    license_no = models.CharField(max_length=50)
    phone_no = models.CharField(max_length=15)
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class SupplierOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='orders')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='supplier_orders')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='supplier_driver')
    date = models.DateField()  # The date of the order
    item_expiry_date = models.DateField(null=True) 
    total_qty = models.IntegerField(default=0)  # Total quantity (calculated)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        self.total_price = self.price * self.total_qty
        super().save(*args, **kwargs)

        # Add the ordered quantity to Stock
        stock, created = Stock.objects.get_or_create(
            item=self.item,
            date=self.date,
            defaults={
                'item_date': self.item_expiry_date,
                
                'total_qty': 0
            }
        )
        stock.total_qty += self.total_qty
        stock.save()

    def __str__(self):
        return f"{self.supplier.name} - {self.item.name} - {self.date}"

    class Meta:
        db_table = 'supplier_order'


class CustomerOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='customer_orders')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='customer_driver')
    date = models.DateField()  # The date of the order
    item_expiry_date = models.DateField(null=True) 
    total_qty = models.IntegerField(default=0)  # Total quantity (calculated)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        self.total_price = self.price * self.total_qty

        with transaction.atomic():
            # Check if there is enough stock before proceeding
            total_stock = Stock.objects.filter(item=self.item).aggregate(total=Sum('total_qty'))['total'] or 0
            if total_stock < self.total_qty:
                raise ValueError(f"Insufficient stock for {self.item.name}")

            super().save(*args, **kwargs)

            # Deduct from the stock
            stocks = Stock.objects.filter(item=self.item)
            remaining_qty = self.total_qty
            print('--------',remaining_qty,total_stock)

            for stock in stocks:
                if remaining_qty <= 0:
                    break

                if stock.total_qty >= remaining_qty:
                    stock.total_qty -= remaining_qty
                    remaining_qty = 0
                else:
                    remaining_qty -= stock.total_qty
                    stock.total_qty = 0
                
                stock.save()

    def __str__(self):
        return f"{self.customer.name} - {self.item.name} - {self.date}"

    class Meta:
        db_table = 'customer_order'


class CustomerItemPrice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='customer_prices')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_prices')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    Discount = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.customer.name} - {self.item.name}"

class SupplierItemPrice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='supplier_prices')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='supplier_prices')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    Discount = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.supplier.name} - {self.item.name}"

class Receipt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    receipt_no = models.CharField(max_length=20, unique=True)
    date = models.DateField()
    customer_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Receipt {self.receipt_no} - {self.customer_name}"

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_no = models.CharField(max_length=20, unique=True)
    date = models.DateField()
    customer_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Payment {self.payment_no} - {self.customer_name}"
