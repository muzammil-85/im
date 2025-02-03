from rest_framework import serializers
from .models import Stock
from .models import Item

class StockSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    piece_per_box = serializers.IntegerField(source='item.piece_per_box', read_only=True)
    daily_total = serializers.SerializerMethodField()

    class Meta:
        model = Stock
        fields = '__all__'

    def get_daily_total(self, obj):
        return Stock.get_daily_total(item_name=obj.item.name, date=obj.date)

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
