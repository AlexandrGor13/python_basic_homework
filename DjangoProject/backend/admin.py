from django.contrib import admin
from backend.models import (
    User,
    Category,
    Product,
    Order,
    OrderItem,
    ShoppingCart,
    CartItem,
    DeliveryAddress,
    Payment,
    Review,
)


# Регистрация пользователей с использованием встроенного интерфейса управления пользователями
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'phone_number']
    search_fields = ['first_name', 'last_name', 'email']
    readonly_fields = ['created_at', 'updated_at']


# Администрирование категорий товаров
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'parent_category']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']


# Администрирование продуктов
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'stock_quantity', 'is_active', 'category']
    list_filter = ['is_active', 'category']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']


# Инлайн отображение позиций заказов
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


# Управление заказами
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ['id', 'user', 'total_amount', 'payment_status', 'order_date']
    list_filter = ['payment_status']
    search_fields = ['user__first_name', 'user__last_name']
    readonly_fields = ['order_date', 'shipped_date', 'completed_date']


# Элементы корзин
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'added_at']
    search_fields = ['product__title']
    readonly_fields = ['added_at']


# Корзины покупателей
@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    filter_horizontal = ['items']  # Удобнее выбирать элементы корзины
    list_display = ['user']


# Административная регистрация модели DeliveryAddress
@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'address_line1', 'city', 'state', 'zip_code', 'country', 'default')  # Поля для отображения в списке
    search_fields = ('address_line1', 'city', 'state', 'country')  # Поисковые поля
    list_filter = ('default',)  # Возможность фильтрации по полю default
    raw_id_fields = ('user',)  # Поле связи с пользователем для удобства выборки большого числа пользователей


# Административная регистрация модели Payment
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'method', 'status', 'timestamp')  # Поля для отображения в списке
    search_fields = ('transaction_id', 'order__id')  # Поиск по номеру транзакции и ID заказа
    list_filter = ('status', 'method')  # Фильтры по статусу и типу платежа
    readonly_fields = ('timestamp',)  # Только для чтения (не изменяется вручную)


# Административная регистрация модели Review
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'comment', 'created_at')  # Поля для отображения в списке
    search_fields = ('user__username', 'product__title', 'comment')  # Поиск по пользователям, продуктам и комментариям
    list_filter = ('rating', 'created_at')  # Фильтр по оценке и дате отзыва
    readonly_fields = ('created_at',)  # Дата создания отзыва доступна только для просмотра
