from rest_framework import viewsets, permissions, status, serializers, exceptions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.db import models
from core.utils import send_dummy_email
from .models import User, Profile, Address, GranularPermission, Wishlist, WishlistItem
from .serializers import (
    UserSerializer, ProfileSerializer, AddressSerializer,
    ChangePasswordSerializer, ForgotPasswordSerializer, ResetPasswordSerializer,
    SuperUserUserSerializer, GranularPermissionSerializer,
    SendOTPSerializer, VerifyOTPSerializer, WishlistSerializer, WishlistItemSerializer
)

class CustomTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})

    @classmethod
    def get_token(cls, user):
        token = RefreshToken.for_user(user)
        # Add custom claims
        token['user_type'] = user.role
        return token

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError({"detail": "Must include 'email' and 'password'."})

        user = authenticate(request=self.context.get('request'), email=email, password=password)
        if not user:
            # Fallback direct lookup
            user_obj = User.objects.filter(email__iexact=email).first()
            if user_obj and user_obj.check_password(password):
                user = user_obj

        if not user:
            raise exceptions.AuthenticationFailed(
                "No active account found with the given credentials",
                code="no_active_account"
            )

        if not user.is_active:
            raise exceptions.AuthenticationFailed(
                "No active account found with the given credentials",
                code="no_active_account"
            )

        refresh = self.get_token(user)

        from .serializers import GranularPermissionSerializer
        permissions_data = GranularPermissionSerializer(user.granular_permissions.all(), many=True).data

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_type': user.role,
            'granular_permissions': permissions_data
        }

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

from rest_framework.decorators import action

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'ADMIN':
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    @action(detail=True, methods=['get'])
    def wishlist(self, request, pk=None):
        user = self.get_object()
        try:
            wishlist = Wishlist.objects.get(user=user)
            return Response(WishlistSerializer(wishlist).data)
        except Wishlist.DoesNotExist:
            return Response({"error": "Wishlist not found"}, status=status.HTTP_404_NOT_FOUND)

class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'ADMIN':
            return Address.objects.all()
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                return Response({'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            user = User.objects.filter(email=email).first()
            if user:
                token = default_token_generator.make_token(user)
                send_dummy_email(email, "Password Reset", f"Your reset token is: {token}")
                return Response({'message': 'Password reset token sent to email.'}, status=status.HTTP_200_OK)
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.data.get('token')
            new_password = serializer.data.get('new_password')
            
            # Simple simulation: finding user who matches token
            for user in User.objects.all():
                if default_token_generator.check_token(user, token):
                    user.set_password(new_password)
                    user.save()
                    return Response({'message': 'Password has been reset.'}, status=status.HTTP_200_OK)
            
            return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

class SuperUserManagementViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SuperUserUserSerializer
    permission_classes = [IsSuperUser]

class GranularPermissionViewSet(viewsets.ModelViewSet):
    queryset = GranularPermission.objects.all()
    serializer_class = GranularPermissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return GranularPermission.objects.all()
        # Non-superusers can only view permissions they are allowed to delegate, 
        # or permissions targeting them.
        return GranularPermission.objects.filter(models.Q(user=user) | models.Q(user__role=user.role, can_delegate=True))

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_superuser:
            serializer.save()
            return
            
        # Non-superusers must have delegation right for the exact same object
        target_user = serializer.validated_data.get('user')
        if target_user.role != user.role and user.role != 'ADMIN':
            raise permissions.exceptions.PermissionDenied("You can only delegate to users with your exact same role.")
            
        content_type = serializer.validated_data.get('content_type')
        object_id = serializer.validated_data.get('object_id')
        
        # Check if user has global delegation, or exact object delegation
        action_flags = {}
        if serializer.validated_data.get('can_view'): action_flags['can_view'] = True
        if serializer.validated_data.get('can_add'): action_flags['can_add'] = True
        if serializer.validated_data.get('can_change'): action_flags['can_change'] = True
        if serializer.validated_data.get('can_delete'): action_flags['can_delete'] = True
        if serializer.validated_data.get('can_delegate'): action_flags['can_delegate'] = True

        has_delegation = GranularPermission.objects.filter(
            models.Q(object_id__isnull=True) | models.Q(object_id=object_id),
            user=user,
            can_delegate=True,
            content_type=content_type,
            **action_flags
        ).exists()
        
        if not has_delegation and user.role != 'ADMIN':
            raise permissions.exceptions.PermissionDenied("You do not have delegation rights for this permission.")
            
        serializer.save()

from django.utils import timezone
from datetime import timedelta
from core.utils import send_dummy_email, send_dummy_sms
import random
from .models import OTPVerification

class SendOTPView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if serializer.is_valid():
            contact_type = serializer.validated_data['contact_type']
            user = request.user
            
            # Basic checks
            if contact_type == 'EMAIL' and user.is_email_verified:
                return Response({'error': 'Email is already verified.'}, status=status.HTTP_400_BAD_REQUEST)
            if contact_type == 'PHONE' and user.is_phone_verified:
                return Response({'error': 'Phone is already verified.'}, status=status.HTTP_400_BAD_REQUEST)
            if contact_type == 'PHONE' and not user.phone_number:
                return Response({'error': 'No phone number associated with account.'}, status=status.HTTP_400_BAD_REQUEST)
                
            otp_code = f"{random.randint(100000, 999999)}"
            
            # Delete any previous OTPs for this user and contact type
            OTPVerification.objects.filter(user=user, contact_type=contact_type).delete()
            
            # Create OTP Verification record
            OTPVerification.objects.create(
                user=user,
                contact_type=contact_type,
                otp_code=otp_code
            )
            
            if contact_type == 'EMAIL':
                send_dummy_email(user.email, "Your DevCommerce OTP", f"Your verification code is: {otp_code}")
                return Response({'message': 'OTP sent to email.'}, status=status.HTTP_200_OK)
            else:
                send_dummy_sms(user.phone_number, f"Your verification code is: {otp_code}")
                return Response({'message': 'OTP sent to phone.'}, status=status.HTTP_200_OK)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            contact_type = serializer.validated_data['contact_type']
            otp_code = serializer.validated_data['otp_code']
            user = request.user
            
            expiry_time = timezone.now() - timedelta(minutes=10)
            otp_record = OTPVerification.objects.filter(
                user=user, 
                contact_type=contact_type, 
                otp_code=otp_code, 
                created_at__gte=expiry_time
            ).first()
            
            if otp_record:
                otp_record.delete()
                
                if contact_type == 'EMAIL':
                    user.is_email_verified = True
                else:
                    user.is_phone_verified = True
                user.save()
                
                return Response({'message': f'{contact_type.capitalize()} verified successfully.'}, status=status.HTTP_200_OK)
                
            return Response({'error': 'Invalid or expired OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from core.permissions import IsCustomerOrAdmin

class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [IsCustomerOrAdmin]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WishlistItemViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistItemSerializer
    permission_classes = [IsCustomerOrAdmin]

    def get_queryset(self):
        return WishlistItem.objects.filter(wishlist__user=self.request.user)

    def perform_create(self, serializer):
        wishlist, _ = Wishlist.objects.get_or_create(user=self.request.user)
        serializer.save(wishlist=wishlist)
