from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path('about/', views.AboutView.as_view(), name='about'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('products/add/', views.ProductCreateView.as_view(), name='add_product'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='edit_product'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='delete_product'),
    path("categories/", views.category_list, name="categories"),
]

