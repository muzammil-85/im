from rest_framework import serializers
from .models import Customer, CustomerItemPrice, CustomerOrder, Driver, Payment, Receipt, Stock, Supplier, SupplierItemPrice, SupplierOrder
from .models import Item
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = User.objects.filter(username=username).first()
            if user and user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return {
                    'username': user.username,
                    'email': user.email,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }
            raise serializers.ValidationError("Invalid credentials.")
        raise serializers.ValidationError("Username and password are required.")

class StockSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    piece_per_box = serializers.IntegerField(source='item.piece_per_box', read_only=True)

    class Meta:
        model = Stock
        fields = '__all__'

    
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class CustomerOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerOrder
        fields = ['id', 'customer', 'item', 'date', 'total_qty', 'item_expiry_date','driver', 'price']

class SupplierOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierOrder
        fields = ['id', 'supplier', 'item', 'date', 'total_qty','item_expiry_date', 'driver', 'price']

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'

class CustomerItemPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerItemPrice
        fields = '__all__'

class SupplierItemPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierItemPrice
        fields = '__all__'

class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'