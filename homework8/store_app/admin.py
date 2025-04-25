from django.contrib import admin
from django.db.models import F

from .models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "price", "created_at", "categories")
    ordering = (
        "name",
        "created_at",
    )
    list_filter = ("name", "price")
    search_fields = ("name", "categories")
    search_help_text = "Поиск по имени и категории"

    @admin.action(description="Увеличить цену на 10%%")
    def price_up(self, request, queryset):
        for product in queryset:
            product.price *= 1.1
            product.save()
        self.message_user(request, "Цена увеличена на 10%")

    @admin.action(description="Снизить цену на 10%%")
    def price_down(self, request, queryset):
        queryset.update(price=F("price") / 0.9)
        self.message_user(request, "Цена снижена на 10%")

    actions = (price_up, price_down)


# def tag_list(self, obj):
#     return ", ".join(o.name for o in obj.tags.all())
#
# tag_list.short_description = 'Теги'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    ordering = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)
    search_help_text = "Поиск по названию категории"
