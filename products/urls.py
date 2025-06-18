from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Category URLs
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<slug:slug>/', views.CategoryDetailView.as_view(), name='category-detail-update-delete'),

    # Product URLs
    path('', views.ProductListCreateView.as_view(), name='product-list-create'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail-update-delete')
]