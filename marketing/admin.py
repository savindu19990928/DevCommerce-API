from django.contrib import admin
from .models import RecommendationTag

@admin.register(RecommendationTag)
class RecommendationTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
