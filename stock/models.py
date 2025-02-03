from django.db import models
from django.db.models import Sum

class Item(models.Model):
    name = models.CharField(max_length=255, unique=True)
    piece_per_box = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'item'


class Stock(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='stocks')
    date = models.DateField()  # The day when the stock is recorded
    item_date = models.DateField()  # Specific item's date
    qty_box = models.IntegerField(default=0)
    qty_piece = models.IntegerField(default=0)
    time = models.TimeField()
    total_qty = models.IntegerField(editable=False)

    def save(self, *args, **kwargs):
        # Ensure piece_per_box is fetched from the related Item table
        self.total_qty = self.qty_box * self.item.piece_per_box + self.qty_piece
        super().save(*args, **kwargs)

    @classmethod
    def get_daily_total(cls, item_name, date):
        """
        Get the total quantity for an item on a specific day.
        """
        total = cls.objects.filter(item__name=item_name, date=date).aggregate(
            daily_total=Sum('total_qty')
        )['daily_total']
        return total or 0

    class Meta:
        db_table = 'stock'
