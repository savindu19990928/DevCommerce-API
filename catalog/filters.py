import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    main_category = django_filters.NumberFilter(
        field_name='categories__id',
        method='filter_main_category',
        help_text='Filter by main category ID (only works if the category has no parent)'
    )

    class Meta:
        model = Product
        fields = ['brand', 'categories', 'is_preorder', 'preorder_arrival_days', 'stock_arrival_days']

    def filter_main_category(self, queryset, name, value):
        return queryset.filter(
            categories__id=value, 
            categories__parent__isnull=True
        ).distinct()
