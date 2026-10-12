from rest_framework import viewsets, permissions, status
from core.permissions import IsCustomerOrHasGranularPermission, HasGranularPermissionOrReadOnly, IsAdminOrReadOnly, IsCustomerOrAdmin
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from django.conf import settings
from .models import Order, OrderItem, Warranty, Refund, Cart, CartItem, Coupon, PhoneCallRequest
from .serializers import (
    OrderSerializer, OrderItemSerializer, WarrantySerializer, RefundSerializer,
    CartSerializer, CartItemSerializer, CouponSerializer, PhoneCallRequestSerializer
)
from core.utils import process_dummy_payment, generate_receipt_pdf, send_dummy_email, log_action
from catalog.models import Product

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsCustomerOrHasGranularPermission]

    def get_queryset(self):
        if self.request.user.role in ['ADMIN', 'ASSISTANT', 'PACKING']:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)
        # Dummy payment gateway usage Example:
        # process_dummy_payment(float(order.total), str(order.order_number))
        
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def resend_receipt(self, request, pk=None):
        order = self.get_object()
        base_url = getattr(settings, 'SITE_URL', 'http://localhost:8000').rstrip('/')
        receipt_link = f"{base_url}/api/orders/receipt/{order.receipt_token}/"
        email = order.guest_email or (order.user.email if order.user else None)
        if email:
            send_dummy_email(email, "Your DevCommerce Receipt (Resend)", f"Download receipt: {receipt_link}")
            return Response({"message": "Receipt resent via email."})
        return Response({"error": "No email associated with this order."}, status=400)
        
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def mark_as_packed(self, request, pk=None):
        if self.request.user.role not in ['ADMIN', 'PACKING']:
            return Response({"error": "Permission denied."}, status=403)
        order = self.get_object()
        
        # Expects {"items": [{"order_item_id": 1, "serial_numbers": [10, 11]}]}
        packing_data = request.data.get('items', [])
        for p_data in packing_data:
            try:
                item = order.items.get(id=p_data['order_item_id'])
                # Assuming SerialNumber model is in inventory and IDs are passed.
                # Here we just set the status, actual serial number logic needs inventory app which is not fully specified here.
                # item.serial_numbers.add(*p_data['serial_numbers'])
            except OrderItem.DoesNotExist:
                pass
                
        order.status = Order.Status.IN_TRANSIT
        order.save()
        log_action("Order packed and handed to delivery", user=self.request.user, order=order)
        return Response({"message": "Order packed and marked as in transit."})

class PhoneCallRequestViewSet(viewsets.ModelViewSet):
    serializer_class = PhoneCallRequestSerializer
    permission_classes = [IsCustomerOrHasGranularPermission]
    
    def get_queryset(self):
        if self.request.user.role in ['ADMIN', 'ASSISTANT']:
            return PhoneCallRequest.objects.all()
        return PhoneCallRequest.objects.filter(user=self.request.user)
        
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WarrantyViewSet(viewsets.ModelViewSet):
    serializer_class = WarrantySerializer
    permission_classes = [IsCustomerOrHasGranularPermission]
    
    def get_queryset(self):
        if self.request.user.role in ['ADMIN', 'ASSISTANT']:
            return Warranty.objects.all()
        return Warranty.objects.filter(order_item__order__user=self.request.user)

class RefundViewSet(viewsets.ModelViewSet):
    serializer_class = RefundSerializer
    permission_classes = [IsCustomerOrHasGranularPermission]
    
    def get_queryset(self):
        if self.request.user.role in ['ADMIN', 'ASSISTANT']:
            return Refund.objects.all()
        return Refund.objects.filter(order__user=self.request.user)

    def perform_create(self, serializer):
        refund = serializer.save(initiated_by=self.request.user)
        log_action(f"Refund initiated for {refund.amount}", user=self.request.user, order=refund.order)

class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        if self.request.user.role == 'ADMIN':
            return Coupon.objects.all()
        return Coupon.objects.filter(active=True)

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsCustomerOrAdmin]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
        cart = self.get_object()
        items = cart.items.all()
        if not items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
            
        promo_code = request.data.get('promo_code')
        discount_pct = 0
        if promo_code:
            from django.utils import timezone
            try:
                coupon = Coupon.objects.get(code=promo_code, active=True, valid_from__lte=timezone.now(), valid_until__gte=timezone.now())
                discount_pct = float(coupon.discount_percentage)
            except Coupon.DoesNotExist:
                return Response({"error": "Invalid or expired promo code"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate max arrival days
        from datetime import timedelta
        from django.utils import timezone
        max_days = 0
        for item in items:
            days = item.product.preorder_arrival_days if item.product.is_preorder else item.product.stock_arrival_days
            if days > max_days:
                max_days = days
        
        estimated_arrival_date = timezone.now().date() + timedelta(days=max_days)

        subtotal = float(sum(item.product.price * item.quantity for item in items))
        discount_amount = subtotal * (discount_pct / 100.0)
        total = subtotal - discount_amount
        
        order = Order.objects.create(
            user=cart.user,
            subtotal=subtotal,
            discount=discount_amount,
            total=total,
            status='PENDING',
            estimated_arrival_date=estimated_arrival_date
        )
        
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                variant=item.variant,
                quantity=item.quantity,
                unit_price=item.product.price,
                subtotal=item.product.price * item.quantity
            )
            
        cart.items.all().delete()
        process_dummy_payment(float(order.total), str(order.order_number))
        log_action("Order placed successfully (Registered User)", user=self.request.user, order=order)
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsCustomerOrAdmin]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)



class GuestCheckoutView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        guest_email = data.get('guest_email')
        guest_name = data.get('guest_name')
        items_data = data.get('items', [])
        
        if not items_data or not guest_email:
            return Response({"error": "Email and items are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        total = 0
        max_days = 0
        for item in items_data:
            product = Product.objects.get(id=item['product_id'])
            total += float(product.price) * int(item['quantity'])
            
            days = product.preorder_arrival_days if product.is_preorder else product.stock_arrival_days
            if days > max_days:
                max_days = days
                
        from datetime import timedelta
        from django.utils import timezone
        estimated_arrival_date = timezone.now().date() + timedelta(days=max_days)
            
        order = Order.objects.create(
            guest_email=guest_email,
            guest_name=guest_name,
            subtotal=total,
            total=total,
            status='PENDING',
            estimated_arrival_date=estimated_arrival_date
        )
        
        for item in items_data:
            product = Product.objects.get(id=item['product_id'])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity'],
                unit_price=product.price,
                subtotal=float(product.price) * int(item['quantity'])
            )
            
        process_dummy_payment(float(order.total), str(order.order_number))
        
        base_url = getattr(settings, 'SITE_URL', 'http://localhost:8000').rstrip('/')
        tracking_link = f"{base_url}/track/{order.guest_tracking_token}"
        receipt_link = f"{base_url}/api/orders/receipt/{order.receipt_token}/"
        send_dummy_email(
            guest_email, 
            "Order Confirmation", 
            f"Track your order here: {tracking_link}\nDownload receipt: {receipt_link}"
        )
        
        log_action("Guest Order placed successfully", user=None, order=order)
        
        return Response({
            "message": "Order placed successfully", 
            "order_number": order.order_number,
            "tracking_token": order.guest_tracking_token
        }, status=status.HTTP_201_CREATED)

class TrackOrderView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, token):
        try:
            order = Order.objects.get(guest_tracking_token=token)
            return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"error": "Invalid tracking token"}, status=status.HTTP_404_NOT_FOUND)

class DownloadReceiptView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, token):
        try:
            order = Order.objects.get(receipt_token=token)
            pdf_bytes = generate_receipt_pdf(order)
            
            response = HttpResponse(pdf_bytes, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="receipt_{order.order_number}.pdf"'
            return response
        except Order.DoesNotExist:
            return Response({"error": "Invalid receipt token"}, status=status.HTTP_404_NOT_FOUND)
