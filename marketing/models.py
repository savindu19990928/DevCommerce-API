from django.db import models
from django.conf import settings
from catalog.models import Product

class RecommendationTag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    products = models.ManyToManyField(Product, related_name='recommendation_tags')

    def __str__(self):
        return self.name
