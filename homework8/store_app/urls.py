from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("products/", views.product_list, name="products"),
    path("products/<int:product_id>/", views.product_detail, name="product_detail"),
    path("categories/", views.category_list, name="categories"),
]
