from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Sum, Count
from orders.models import Order
from catalog.models import Product

class ReportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role != 'ADMIN':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only admins can access reports.")
            
        # Basic aggregate data for the admin dashboard reports
        total_revenue = Order.objects.filter(payment_status='SUCCESS').aggregate(Sum('total'))['total__sum'] or 0
        total_orders = Order.objects.count()
        total_products = Product.objects.count()
        low_stock_products = Product.objects.filter(stock_arrival_days__gt=0).count() # Mock logic
        
        return Response({
            "financials": {
                "total_revenue": total_revenue,
                "total_orders": total_orders
            },
            "inventory": {
                "total_products": total_products,
                "low_stock_alerts": low_stock_products
            },
            "message": "Full PDF/CSV exports can be built from this endpoint."
        })
