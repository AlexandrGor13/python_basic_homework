from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm, PostModelForm
from .models import Product, Category


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

def add_product(request):
    if request.method == 'POST':
        form = PostModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('posts')
    else:
        form = PostModelForm()

    context = {'form': form, 'title': 'Добавить товар'}
    return render(request, 'store_app/add_product.html', context=context)


def edit_product(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = PostModelForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = PostModelForm(instance=product)

    context = {'form': form, 'title': 'Добавить товар'}
    return render(request, 'store_app/edit_product.html', context)


def category_list(request):
    categories = Category.objects.all()
    context = {"categories": categories}
    return render(request, "store_app/category_list.html", context=context)
