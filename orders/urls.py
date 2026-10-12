from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    OrderViewSet, WarrantyViewSet, RefundViewSet,
    CartViewSet, CartItemViewSet,
    GuestCheckoutView, TrackOrderView, DownloadReceiptView, CouponViewSet, PhoneCallRequestViewSet
)

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'warranties', WarrantyViewSet, basename='warranty')
router.register(r'refunds', RefundViewSet, basename='refund')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'cart-items', CartItemViewSet, basename='cartitem')
router.register(r'coupons', CouponViewSet, basename='coupon')
router.register(r'phone-call-requests', PhoneCallRequestViewSet, basename='phonecallrequest')

urlpatterns = [
    path('guest-checkout/', GuestCheckoutView.as_view(), name='guest-checkout'),
    path('track/<uuid:token>/', TrackOrderView.as_view(), name='track-order'),
    path('receipt/<uuid:token>/', DownloadReceiptView.as_view(), name='download-receipt'),
    path('', include(router.urls)),
]
