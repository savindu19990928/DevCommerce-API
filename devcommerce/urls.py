from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from core.views import ReportView

def health_check(request):
    return HttpResponse("OK")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/catalog/', include('catalog.urls')),
    path('api/inventory/', include('inventory.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/support/', include('support.urls')),
    path('api/marketing/', include('marketing.urls')),
    path('api/reports/', ReportView.as_view(), name='reports'),
    path('health/', health_check),
]
