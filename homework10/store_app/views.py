from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import ProductModelForm
from .models import Product, Category

def index(request):
    return render(request, "store_app/index.html")


class AboutView(TemplateView):
    template_name = 'store_app/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'О нас'
        context['content'] = 'Добро пожаловать на наш сайт'
        return context


class ProductListView(ListView):
    """Представление для отображения списка товаров"""
    model = Product
    template_name = 'store_app/product_list.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    """Представление для отображения деталей товара"""
    model = Product
    template_name = 'store_app/product_detail.html'
    context_object_name = 'product'

    # def get(self, request, *args, **kwargs):
    #     product = self.get_object()
    #     return super().get(request, *args, **kwargs)


class ProductCreateView(CreateView):
    """Представление для создания нового товара"""
    model = Product
    template_name = 'store_app/add_product.html'
    form_class = ProductModelForm
    success_url = reverse_lazy('product')

    def form_valid(self, form):
        messages.success(self.request, 'Товар успешно создан')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление товара'
        return context


class ProductUpdateView(UpdateView):
    """Представление для обновления товара"""
    model = Product
    template_name = 'store_app/edit_product.html'
    form_class = ProductModelForm
    success_url = reverse_lazy('products')

    def form_valid(self, form):
        messages.success(self.request, 'Товар успешно обновлен')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Обновление товара'
        return context


class ProductDeleteView(DeleteView):
    """Представление для удаления товара"""
    model = Product
    template_name = 'store_app/delete_product.html'
    success_url = reverse_lazy('products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление товара'
        return context


def category_list(request):
    categories = Category.objects.all()
    context = {"categories": categories}
    return render(request, "store_app/category_list.html", context=context)
