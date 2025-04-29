from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as get_txt

from config import settings




class User(models.Model):
    """Модель пользователя"""
    username = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    first_name = models.CharField(get_txt('Имя'), max_length=150)
    last_name = models.CharField(get_txt('Фамилия'), max_length=150)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = get_txt('Пользователь')
        verbose_name_plural = get_txt('Пользователи')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Category(models.Model):
    """Категория продуктов"""
    name = models.CharField(max_length=255)
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = get_txt('Категория')
        verbose_name_plural = get_txt('Категории')

    def __str__(self):
        return self.name


class Product(models.Model):
    """Продукт"""
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    stock_quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = get_txt('Продукт')
        verbose_name_plural = get_txt('Продукты')

    def __str__(self):
        return self.title


class Order(models.Model):
    """Заказ"""
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    user = models.ForeignKey('User', on_delete=models.PROTECT)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=50, choices=[
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    ])
    shipping_address = models.ForeignKey('DeliveryAddress', on_delete=models.PROTECT)
    order_date = models.DateTimeField(auto_now_add=True)
    shipped_date = models.DateTimeField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = get_txt('Заказ')
        verbose_name_plural = get_txt('Заказы')

    def __str__(self):
        return f'Order #{self.pk}'


class OrderItem(models.Model):
    """Позиция заказа"""
    order = models.ForeignKey('Order', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = get_txt('Элемент заказа')
        verbose_name_plural = get_txt('Элементы заказа')

    def __str__(self):
        return f'{self.product} x {self.quantity}'


class ShoppingCart(models.Model):
    """Корзина покупок"""
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    items = models.ManyToManyField('CartItem')

    class Meta:
        verbose_name = get_txt('Корзина покупок')
        verbose_name_plural = get_txt('Корзины покупок')

    def __str__(self):
        return f'Корзина покупок {self.user}'


class CartItem(models.Model):
    """Элемент корзины"""
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Время добавления")

    class Meta:
        verbose_name = "Позиция корзины"
        verbose_name_plural = "Позиции корзины"

    def __str__(self):
        return f'{self.product} x {self.quantity}'

    @property
    def total_price(self):
        """
        Вычисляет полную стоимость текущего товара в корзине
        """
        return self.quantity * self.product.price


class DeliveryAddress(models.Model):
    """Адрес доставки"""
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    default = models.BooleanField(default=False)

    class Meta:
        verbose_name = get_txt('Адрес доставки')
        verbose_name_plural = get_txt('Адреса доставки')

    def __str__(self):
        return f'{self.address_line1}, {self.city}, {self.country}'


class Payment(models.Model):
    """Платёж"""
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=50, choices=[
        ('card', 'Card'),
        ('cash', 'Cash'),
        ('paypal', 'PayPal'),
    ])
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50, choices=[
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('canceled', 'Canceled'),
    ])
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = get_txt('Платёж')
        verbose_name_plural = get_txt('Платежи')

    def __str__(self):
        return f'Оплата за заказ #{self.order.pk}'


class Review(models.Model):
    """Отзыв клиента"""
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[
        (1, 'Very Bad'),
        (2, 'Bad'),
        (3, 'Average'),
        (4, 'Good'),
        (5, 'Excellent'),
    ])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = get_txt('Отзыв')
        verbose_name_plural = get_txt('Отзывы')

    def __str__(self):
        return f'Отзыв {self.user} о {self.product}'
