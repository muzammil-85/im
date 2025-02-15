import datetime
from rest_framework import viewsets
from .models import Customer, CustomerItemPrice, CustomerOrder, Driver, Item, Payment, Receipt, Stock, Supplier, SupplierItemPrice, SupplierOrder
from .serializer import CustomerItemPriceSerializer, CustomerOrderSerializer, CustomerSerializer, DriverSerializer, ItemSerializer, PaymentSerializer, ReceiptSerializer, StockSerializer, SupplierItemPriceSerializer, SupplierOrderSerializer, SupplierSerializer
import pandas as pd
from django.http import HttpResponse
from .models import Stock
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime, timedelta


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
class CustomerOrderViewSet(viewsets.ModelViewSet):
    queryset = CustomerOrder.objects.all()
    serializer_class = CustomerOrderSerializer

class SupplierOrderViewSet(viewsets.ModelViewSet):
    queryset = SupplierOrder.objects.all()
    serializer_class = SupplierOrderSerializer

class CustomerItemPriceViewSet(viewsets.ModelViewSet):
    queryset = CustomerItemPrice.objects.all()
    serializer_class = CustomerItemPriceSerializer

class SupplierItemPriceViewSet(viewsets.ModelViewSet):
    queryset = SupplierItemPrice.objects.all()
    serializer_class = SupplierItemPriceSerializer

class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class CashbookView(APIView):
    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not start_date or not end_date:
            return Response({"error": "Please provide both start_date and end_date"}, status=400)

        try:
            # Convert strings to date objects
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
            day_before_start_date = (start_date_obj - timedelta(days=1)).strftime("%Y-%m-%d")
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        # Fetch all receipts (credit transactions) in the date range
        receipts = Receipt.objects.filter(date__range=[start_date, end_date])
        credit = receipts.aggregate(Sum('amount'))['amount__sum'] or 0

        # Fetch all purchase payments (debit transactions) in the date range
        payments = Payment.objects.filter(date__range=[start_date, end_date])
        debit = payments.aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Fetch all receipts (credit transactions) before the end date
        past_receipts = Receipt.objects.filter(date__range=['2025-01-01', day_before_start_date])
        total_credit = past_receipts.aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Fetch all purchase payments (debit transactions) before the end date
        past_payments = Payment.objects.filter(date__range=['2025-01-01', day_before_start_date])
        total_debit = past_payments.aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Calculate opening and closing balance
        opening_balance = total_credit - total_debit
        closing_balance = (opening_balance + credit) - debit

        # Serialize receipts and payments
        receipt_data = ReceiptSerializer(receipts, many=True).data
        payment_data = PaymentSerializer(payments, many=True).data

        # Construct response
        cashbook_data = {
            "date_range": f"{start_date} to {end_date}",
            "opening_balance": opening_balance,
            "total_credit": credit,
            "total_debit": debit,
            "closing_balance": closing_balance,
            "receipts": receipt_data,
            "payments": payment_data,
        }

        return Response(cashbook_data)

class LedgerView(APIView):
    def get(self, request):
        entity_type = request.query_params.get('type')  # 'customer' or 'supplier'
        name = request.query_params.get('name')  # Name of customer or supplier
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not entity_type or not start_date or not end_date:
            return Response({"error": "Please provide type (customer/supplier), start_date, and end_date"}, status=400)

        try:
            # Convert strings to date objects
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
            day_before_start_date = (start_date_obj - timedelta(days=1)).strftime("%Y-%m-%d")
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)
        ledger_data = {}

        if entity_type.lower() == "customer":
            # Fetch receipts (payments received from customers)
            receipts = Receipt.objects.filter(date__range=[start_date, end_date])
            if name:
                receipts = receipts.filter(customer_name=name)

            total_receipts = receipts.aggregate(Sum('amount'))['amount__sum'] or 0
            receipt_data = ReceiptSerializer(receipts, many=True).data

            # Fetch customer orders
            customer_orders = CustomerOrder.objects.filter(date__range=[start_date, end_date])
            if name:
                customer_orders = customer_orders.filter(customer__name=name)

            total_customer_orders = customer_orders.aggregate(Sum('total_price'))['total_price__sum'] or 0
            customer_order_data = CustomerOrderSerializer(customer_orders, many=True).data
            
            # Fetch all receipts (credit transactions) before the end date
            past_receipts = Receipt.objects.filter(date__range=['2025-01-01', day_before_start_date])
            total_credit = past_receipts.aggregate(Sum('amount'))['amount__sum'] or 0
            past_customer_orders = CustomerOrder.objects.filter(date__range=['2025-01-01', day_before_start_date])
            total_customer_bill = past_customer_orders.aggregate(Sum('total_price'))['total_price__sum'] or 0
            
            # Calculate opening and closing balance
            opening_balance = total_customer_bill - total_credit
            closing_balance = (opening_balance + total_customer_orders) - total_receipts

            ledger_data = {
                "type": "customer",
                "name": name or "All Customers",
                "date_range": f"{start_date} to {end_date}",
                "total_receipts": total_receipts,
                "total_receipts": total_customer_orders,
                "opening_balance": opening_balance,
                "closing_balance": closing_balance,
                "receipts": receipt_data,
                "customer_orders": customer_order_data,
            }

        elif entity_type.lower() == "supplier":
            # Fetch payments (payments made to suppliers)
            payments = Payment.objects.filter(date__range=[start_date, end_date])
            if name:
                payments = payments.filter(customer_name=name)

            total_payments = payments.aggregate(Sum('amount'))['amount__sum'] or 0
            payment_data = PaymentSerializer(payments, many=True).data

            # Fetch supplier orders
            supplier_orders = SupplierOrder.objects.filter(date__range=[start_date, end_date])
            if name:
                supplier_orders = supplier_orders.filter(supplier__name=name)

            total_supplier_orders = supplier_orders.aggregate(Sum('total_price'))['total_price__sum'] or 0
            supplier_order_data = SupplierOrderSerializer(supplier_orders, many=True).data

            ledger_data = {
                "type": "supplier",
                "name": name or "All Suppliers",
                "date_range": f"{start_date} to {end_date}",
                "total_payments": total_payments,
                "total_orders": total_supplier_orders,
                "payments": payment_data,
                "supplier_orders": supplier_order_data,
            }

        else:
            return Response({"error": "Invalid type. Use 'customer' or 'supplier'."}, status=400)

        return Response(ledger_data)
    
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

class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer