from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("products/", views.product_list, name="products"),
    path('products/add/', views.add_product, name='add_product'),
    path("products/<int:product_id>/", views.product_detail, name="product_detail"),
    path('products/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path("categories/", views.category_list, name="categories"),
]

