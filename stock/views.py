from rest_framework import viewsets
from .models import Item, Stock
from .serializer import ItemSerializer, StockSerializer
import pandas as pd
from django.http import HttpResponse
from .models import Stock

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

def export_stock_to_excel(request, date):
    # Query the stock data for the given date
    stocks = Stock.objects.filter(date=date).select_related('item')
    print('stock=',stocks)
    # Create a list of dictionaries for the data
    data = [
        {
            "Item Name": stock.item.name,
            "Date": stock.date,
            "Item Date": stock.item_date,
            "Qty (Boxes)": stock.qty_box,
            "Qty (Pieces)": stock.qty_piece,
            "Pieces per Box": stock.item.piece_per_box,
            "Total Qty": stock.total_qty,
            "Time": stock.time,
        }
        for stock in stocks
    ]
    print('data========',data)
    # Convert data to a pandas DataFrame
    df = pd.DataFrame(data)

    # Create an Excel file in memory
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="stock_data_{date}.xlsx"'

    # Save the DataFrame to the response as an Excel file
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Stock Data')

    return response
