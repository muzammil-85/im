from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import (
    Customer, CustomerItemPrice, CustomerOrder, Driver, Item, Payment, Receipt, Stock, Supplier, SupplierItemPrice, SupplierOrder
)
from .serializer import (
    CustomerItemPriceSerializer, CustomerOrderSerializer, CustomerSerializer, DriverSerializer, ItemSerializer,
    PaymentSerializer, ReceiptSerializer, StockSerializer, SupplierItemPriceSerializer, SupplierOrderSerializer, SupplierSerializer
)
import pandas as pd
from django.http import HttpResponse
from .models import Stock
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime, timedelta
from rest_framework.permissions import IsAuthenticated

from rest_framework.permissions import BasePermission
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import LoginSerializer

class LoginAPI(APIView): 
    permission_classes = [AllowAny] 
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# class IsAdminUser(BasePermission):
#     def has_permission(self, request, view):
#         return request.user and request.user.is_staff
# Item ViewSet
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]  

    @action(detail=False, methods=['get'])
    def list_items(self, request):
        items = self.get_queryset()
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def retrieve_item(self, request, pk=None):
        item = self.get_object()
        serializer = self.get_serializer(item)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def create_item(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put', 'patch'])
    def update_item(self, request, pk=None):
        item = self.get_object()
        serializer = self.get_serializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_item(self, request, pk=None):
        item = self.get_object()
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Stock ViewSet
class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated] 

    @action(detail=False, methods=['get'])
    def list_stocks(self, request):
        stocks = self.get_queryset()
        serializer = self.get_serializer(stocks, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def retrieve_stock(self, request, pk=None):
        stock = self.get_object()
        serializer = self.get_serializer(stock)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def create_stock(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put', 'patch'])
    def update_stock(self, request, pk=None):
        stock = self.get_object()
        serializer = self.get_serializer(stock, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_stock(self, request, pk=None):
        stock = self.get_object()
        stock.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Customer ViewSet
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated] 

    @action(detail=False, methods=['get'])
    def list_customers(self, request):
        customers = self.get_queryset()
        serializer = self.get_serializer(customers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def retrieve_customer(self, request, pk=None):
        customer = self.get_object()
        serializer = self.get_serializer(customer)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def create_customer(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put', 'patch'])
    def update_customer(self, request, pk=None):
        customer = self.get_object()
        serializer = self.get_serializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_customer(self, request, pk=None):
        customer = self.get_object()
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Supplier ViewSet
class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated] 

    @action(detail=False, methods=['get'])
    def list_suppliers(self, request):
        suppliers = self.get_queryset()
        serializer = self.get_serializer(suppliers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def retrieve_supplier(self, request, pk=None):
        supplier = self.get_object()
        serializer = self.get_serializer(supplier)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def create_supplier(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put', 'patch'])
    def update_supplier(self, request, pk=None):
        supplier = self.get_object()
        serializer = self.get_serializer(supplier, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_supplier(self, request, pk=None):
        supplier = self.get_object()
        supplier.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# CustomerOrder ViewSet
class CustomerOrderViewSet(viewsets.ModelViewSet):
    queryset = CustomerOrder.objects.all()
    serializer_class = CustomerOrderSerializer
    permission_classes = [IsAuthenticated] 

    @action(detail=False, methods=['get'])
    def list_customer_orders(self, request):
        orders = self.get_queryset()
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def retrieve_customer_order(self, request, pk=None):
        order = self.get_object()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def create_customer_order(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put', 'patch'])
    def update_customer_order(self, request, pk=None):
        order = self.get_object()
        serializer = self.get_serializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_customer_order(self, request, pk=None):
        order = self.get_object()
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# SupplierOrder ViewSet
class SupplierOrderViewSet(viewsets.ModelViewSet):
    queryset = SupplierOrder.objects.all()
    serializer_class = SupplierOrderSerializer
    permission_classes = [IsAuthenticated] 

    @action(detail=False, methods=['get'])
    def list_supplier_orders(self, request):
        orders = self.get_queryset()
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def retrieve_supplier_order(self, request, pk=None):
        order = self.get_object()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def create_supplier_order(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put', 'patch'])
    def update_supplier_order(self, request, pk=None):
        order = self.get_object()
        serializer = self.get_serializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_supplier_order(self, request, pk=None):
        order = self.get_object()
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Driver ViewSet
class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated] 

    @action(detail=False, methods=['get'])
    def list_drivers(self, request):
        drivers = self.get_queryset()
        serializer = self.get_serializer(drivers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def retrieve_driver(self, request, pk=None):
        driver = self.get_object()
        serializer = self.get_serializer(driver)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def create_driver(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put', 'patch'])
    def update_driver(self, request, pk=None):
        driver = self.get_object()
        serializer = self.get_serializer(driver, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_driver(self, request, pk=None):
        driver = self.get_object()
        driver.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# CustomerItemPrice ViewSet
class CustomerItemPriceViewSet(viewsets.ModelViewSet):
    queryset = CustomerItemPrice.objects.all()
    serializer_class = CustomerItemPriceSerializer
    permission_classes = [IsAuthenticated] 

    @action(detail=False, methods=['get'])
    def list_customer_item_prices(self, request):
        prices = self.get_queryset()
        serializer = self.get_serializer(prices, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def retrieve_customer_item_price(self, request, pk=None):
        price = self.get_object()
        serializer = self.get_serializer(price)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def create_customer_item_price(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put', 'patch'])
    def update_customer_item_price(self, request, pk=None):
        price = self.get_object()
        serializer = self.get_serializer(price, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_customer_item_price(self, request, pk=None):
        price = self.get_object()
        price.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# SupplierItemPrice ViewSet
class SupplierItemPriceViewSet(viewsets.ModelViewSet):
    queryset = SupplierItemPrice.objects.all()
    serializer_class = SupplierItemPriceSerializer
    permission_classes = [IsAuthenticated] 

    @action(detail=False, methods=['get'])
    def list_supplier_item_prices(self, request):
        prices = self.get_queryset()
        serializer = self.get_serializer(prices, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def retrieve_supplier_item_price(self, request, pk=None):
        price = self.get_object()
        serializer = self.get_serializer(price)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def create_supplier_item_price(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put', 'patch'])
    def update_supplier_item_price(self, request, pk=None):
        price = self.get_object()
        serializer = self.get_serializer(price, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_supplier_item_price(self, request, pk=None):
        price = self.get_object()
        price.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Receipt ViewSet
class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    permission_classes = [IsAuthenticated] 

    @action(detail=False, methods=['get'])
    def list_receipts(self, request):
        receipts = self.get_queryset()
        serializer = self.get_serializer(receipts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def retrieve_receipt(self, request, pk=None):
        receipt = self.get_object()
        serializer = self.get_serializer(receipt)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def create_receipt(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put', 'patch'])
    def update_receipt(self, request, pk=None):
        receipt = self.get_object()
        serializer = self.get_serializer(receipt, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_receipt(self, request, pk=None):
        receipt = self.get_object()
        receipt.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Payment ViewSet
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated] 

    @action(detail=False, methods=['get'])
    def list_payments(self, request):
        payments = self.get_queryset()
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def retrieve_payment(self, request, pk=None):
        payment = self.get_object()
        serializer = self.get_serializer(payment)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def create_payment(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put', 'patch'])
    def update_payment(self, request, pk=None):
        payment = self.get_object()
        serializer = self.get_serializer(payment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_payment(self, request, pk=None):
        payment = self.get_object()
        payment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CashbookView(APIView):
    permission_classes = [IsAuthenticated] 
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
            
            # Fetch all receipts to calculate grand total
            grand_total_receipts = Receipt.objects.all()
            grand_total_credit = grand_total_receipts.aggregate(Sum('amount'))['amount__sum'] or 0
            grand_total_customer_orders = CustomerOrder.objects.all()
            grand_total_customer_bill = grand_total_customer_orders.aggregate(Sum('total_price'))['total_price__sum'] or 0
            
            # Calculate opening and closing balance
            grand_total_balance = grand_total_customer_bill - grand_total_credit

            ledger_data = {
                "type": "customer",
                "name": name or "All Customers",
                "date_range": f"{start_date} to {end_date}",
                "total_receipts": total_receipts,
                "total_bill_receipts": total_customer_orders,
                "opening_balance": opening_balance,
                "closing_balance": closing_balance,
                "grand_total_balance": grand_total_balance,
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

            # Fetch all receipts to calculate grand total
            grand_total_payments = Payment.objects.all()
            grand_total_payments = grand_total_payments.aggregate(Sum('amount'))['amount__sum'] or 0
            grand_total_supplier_orders = SupplierOrder.objects.all()
            grand_total_supplier_bill = grand_total_supplier_orders.aggregate(Sum('total_price'))['total_price__sum'] or 0
            
            # Calculate opening and closing balance
            grand_total_balance = grand_total_supplier_bill - grand_total_payments
            ledger_data = {
                "type": "supplier",
                "name": name or "All Suppliers",
                "date_range": f"{start_date} to {end_date}",
                "total_payments": total_payments,
                "total_purchase_orders": total_supplier_orders,
                "grand_total_balance": grand_total_balance,
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