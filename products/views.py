from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer

class ProductListCreateView(generics.ListCreateAPIView):
    """
    GET: List all products
    POST: Create a new product
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a single product by slug
    PUT: Update a product
    DELETE: Delete a product
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug' # use slugs instead of pk for lookups



