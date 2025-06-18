from django.urls import path
from .views import ProductListCreateView, ProductDetailView

app_name = 'products'

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list-create'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product-detail-update-delete')
]