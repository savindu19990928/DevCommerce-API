from django.contrib import admin
from .models import Category, Brand, Product, ProductImage, ProductSpecification, ProductVariant, Review, Question, Answer

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug')
    list_filter = ('parent',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'brand', 'price', 'cost_price', 'status', 'is_preorder', 'minimum_stock_level', 'expiry_date')
    list_filter = ('status', 'brand', 'is_preorder', 'categories')
    search_fields = ('name', 'sku')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductSpecificationInline, ProductVariantInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'rating')
    search_fields = ('product__name', 'user__username', 'comment')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'text', 'is_approved', 'created_at')
    list_filter = ('is_approved',)
    search_fields = ('product__name', 'user__username', 'text')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'user', 'text', 'is_approved', 'created_at')
    list_filter = ('is_approved',)
    search_fields = ('question__text', 'user__username', 'text')
