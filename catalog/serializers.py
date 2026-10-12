from rest_framework import serializers
from .models import Category, Brand, Product, ProductImage, ProductSpecification, ProductVariant, Review, Question, Answer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'image', 'is_primary', 'order']

    def validate(self, attrs):
        product = attrs.get('product') or (self.instance.product if self.instance else None)
        if product:
            query = ProductImage.objects.filter(product=product)
            if self.instance and self.instance.pk:
                query = query.exclude(pk=self.instance.pk)
            if query.count() >= 5:
                raise serializers.ValidationError({"error": "A product cannot have more than 5 photos."})
        return attrs

class ProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = ['id', 'key', 'value']

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    specifications = ProductSpecificationSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    brand_details = BrandSerializer(source='brand', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
        read_only_fields = ['user', 'is_approved']

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ['user', 'is_approved']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['user', 'is_approved']
