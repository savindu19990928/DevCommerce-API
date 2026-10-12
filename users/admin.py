from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Address, Profile, GranularPermission, OTPVerification, Wishlist, WishlistItem

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_phone_verified', 'is_staff')
    list_filter = ('role', 'is_phone_verified', 'is_email_verified', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'phone_number')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Info', {'fields': ('role', 'phone_number', 'is_phone_verified', 'is_email_verified')}),
        ('Notifications', {'fields': ('notify_order_email', 'notify_order_sms', 'notify_receipt_email', 'notify_receipt_sms', 'notify_promotions_email', 'notify_promotions_sms')}),
    )

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'recipient_name', 'city', 'country', 'is_default')
    list_filter = ('country', 'state_province', 'is_default')
    search_fields = ('recipient_name', 'street_address', 'phone_number', 'user__username')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)

@admin.register(GranularPermission)
class GranularPermissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'object_id', 'can_view', 'can_add', 'can_change', 'can_delete', 'can_delegate')
    list_filter = ('can_delegate', 'content_type')
    search_fields = ('user__username',)

@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact_type', 'otp_code', 'created_at')
    list_filter = ('contact_type', 'created_at')
    search_fields = ('user__username', 'otp_code')

class WishlistItemInline(admin.TabularInline):
    model = WishlistItem
    extra = 0

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    inlines = [WishlistItemInline]
