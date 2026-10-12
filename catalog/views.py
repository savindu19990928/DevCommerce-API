from rest_framework import viewsets, permissions, status, parsers, filters
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category, Brand, Product, ProductImage, Review, Question, Answer
from .serializers import (
    CategorySerializer, BrandSerializer, ProductSerializer, ProductImageSerializer,
    ReviewSerializer, QuestionSerializer, AnswerSerializer
)
from .filters import ProductFilter
import django_filters.rest_framework
from core.permissions import HasGranularPermissionOrReadOnly, IsAdminOrReadOnly, IsOwnerOrAdmin

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['parent']

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdminOrReadOnly]

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'sku', 'description']

    def get_queryset(self):
        if self.request.user and self.request.user.is_authenticated and self.request.user.role in ['ADMIN', 'STOCK']:
            return Product.objects.all()
        return Product.objects.filter(status='ACTIVE')

    @action(detail=True, methods=['post'], parser_classes=[parsers.MultiPartParser, parsers.FormParser])
    def upload_images(self, request, pk=None):
        product = self.get_object()
        images = request.FILES.getlist('images') or request.FILES.getlist('image')
        if not images:
            return Response(
                {"error": "No image files provided. Pass one or more files in 'images'."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        current_count = product.images.count()
        if current_count + len(images) > 5:
            return Response({
                "error": f"Cannot upload {len(images)} photos. Product currently has {current_count} photos. Maximum allowed is 5 photos per product."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        created_images = []
        for idx, img_file in enumerate(images):
            is_primary = (current_count == 0 and idx == 0)
            product_img = ProductImage.objects.create(
                product=product,
                image=img_file,
                order=current_count + idx,
                is_primary=is_primary
            )
            created_images.append(product_img)
            
        return Response(
            ProductImageSerializer(created_images, many=True, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['product', 'is_primary']

    def create(self, request, *args, **kwargs):
        images = request.FILES.getlist('images') or request.FILES.getlist('image')
        product_id = request.data.get('product')
        
        if not product_id:
            return Response({"product": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"product": ["Invalid product ID."]}, status=status.HTTP_400_BAD_REQUEST)

        if not images:
            return Response({"image": ["No image file provided."]}, status=status.HTTP_400_BAD_REQUEST)

        current_count = product.images.count()
        if current_count + len(images) > 5:
            return Response({
                "error": f"Cannot upload {len(images)} photos. Product currently has {current_count} photos. Maximum allowed is 5 photos per product."
            }, status=status.HTTP_400_BAD_REQUEST)

        created_images = []
        is_primary_req = request.data.get('is_primary', False)
        if isinstance(is_primary_req, str):
            is_primary_req = is_primary_req.lower() in ['true', '1']

        for idx, img_file in enumerate(images):
            is_primary = is_primary_req if (len(images) == 1) else (current_count == 0 and idx == 0)
            product_img = ProductImage.objects.create(
                product=product,
                image=img_file,
                order=current_count + idx,
                is_primary=is_primary
            )
            created_images.append(product_img)

        if len(created_images) == 1:
            return Response(ProductImageSerializer(created_images[0], context={'request': request}).data, status=status.HTTP_201_CREATED)
        return Response(ProductImageSerializer(created_images, many=True, context={'request': request}).data, status=status.HTTP_201_CREATED)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.filter(is_approved=True)
    serializer_class = ReviewSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        if not self.request.user.is_phone_verified:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You must verify your phone number to leave a review.")
        serializer.save(user=self.request.user)

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.filter(is_approved=True)
    serializer_class = QuestionSerializer
    permission_classes = [IsOwnerOrAdmin]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.filter(is_approved=True)
    serializer_class = AnswerSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class HomepageView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        base_qs = Product.objects.filter(status='ACTIVE')
        
        popular = base_qs.order_by('-updated_at')[:5]
        trending = base_qs.order_by('-created_at')[:5]
        on_sale = base_qs.filter(sale_price__isnull=False)[:5]
        
        recommended = []
        if request.user.is_authenticated:
            recommended = base_qs.order_by('?')[:5]
            
        serializer_context = {'request': request}
        return Response({
            "popular": ProductSerializer(popular, many=True, context=serializer_context).data,
            "trending": ProductSerializer(trending, many=True, context=serializer_context).data,
            "on_sale": ProductSerializer(on_sale, many=True, context=serializer_context).data,
            "recommended": ProductSerializer(recommended, many=True, context=serializer_context).data if recommended else []
        })
