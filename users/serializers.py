from rest_framework import serializers
from .models import User, Profile, Address, GranularPermission, Wishlist, WishlistItem

class WishlistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistItem
        fields = '__all__'
        read_only_fields = ['wishlist']

class WishlistSerializer(serializers.ModelSerializer):
    items = WishlistItemSerializer(many=True, read_only=True)

    class Meta:
        model = Wishlist
        fields = '__all__'
        read_only_fields = ['user']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['profile_photo', 'bio']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone_number', 'is_phone_verified', 'is_email_verified', 'profile']
        read_only_fields = ['role', 'is_phone_verified', 'is_email_verified']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ['user']

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

from django.contrib.contenttypes.models import ContentType

class GranularPermissionSerializer(serializers.ModelSerializer):
    model_name = serializers.CharField(write_only=True, required=False, help_text="e.g., 'product', 'category'")

    class Meta:
        model = GranularPermission
        fields = '__all__'
        read_only_fields = ['content_type']

    def validate(self, attrs):
        model_name = attrs.pop('model_name', None)
        if model_name:
            try:
                ctype = ContentType.objects.get(model=model_name.lower())
                attrs['content_type'] = ctype
            except ContentType.DoesNotExist:
                raise serializers.ValidationError({"model_name": "Invalid model name."})
            except ContentType.MultipleObjectsReturned:
                raise serializers.ValidationError({"model_name": "Multiple models match."})
        return attrs

class SuperUserUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone_number', 'is_phone_verified', 'is_email_verified', 'profile']
        # Superusers can edit roles
        read_only_fields = ['is_phone_verified', 'is_email_verified']

class SendOTPSerializer(serializers.Serializer):
    contact_type = serializers.ChoiceField(choices=['EMAIL', 'PHONE'])

class VerifyOTPSerializer(serializers.Serializer):
    contact_type = serializers.ChoiceField(choices=['EMAIL', 'PHONE'])
    otp_code = serializers.CharField(max_length=6, min_length=6)
