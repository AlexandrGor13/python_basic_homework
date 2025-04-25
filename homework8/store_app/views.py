from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from store_app.models import Product, Category


# Create your views here.


def index(request):
    return render(request, "store_app/index.html")


def about(request):
    return HttpResponse("About")


def product_list(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "store_app/product_list.html", context=context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {"product": product}
    return render(request, "store_app/product_detail.html", context=context)


def category_list(request):
    categories = Category.objects.all()
    context = {"categories": categories}
    return render(request, "store_app/category_list.html", context=context)
