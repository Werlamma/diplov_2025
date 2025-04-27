import stripe
from django.db import models
from users.models import User
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название категории")
    slug = models.SlugField(unique=True, verbose_name="Слаг (URL)")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products',
                                 verbose_name="Категория")
    name = models.CharField(max_length=255, verbose_name="Название продукта")
    slug = models.SlugField(unique=True, verbose_name="Слаг (URL)")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to='products/', verbose_name="Изображение")
    stripe_product_price_id = models.CharField(max_length=128, blank=True, null=True, verbose_name="Цена для Страйпа")
    characteristics = models.TextField(verbose_name="Характеристики",
                                       help_text="Каждую характеристику вводите с новой строки")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']
        super().save(*args, **kwargs)

    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'], unit_amount=round(self.price * 100), currency='rub')
        return stripe_product_price

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Basket', verbose_name="Пользователь")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def sum(self):
        """Возвращает общую стоимость товара в корзине (цена * количество)"""
        return self.product.price * self.quantity

    @staticmethod
    def total_sum(user):
        """Возвращает общую стоимость всех товаров в корзине пользователя"""
        baskets = Basket.objects.filter(user=user)
        return sum(basket.sum() for basket in baskets)

    @staticmethod
    def total_quantity(user):
        """Возвращает общее количество товаров в корзине пользователя"""
        baskets = Basket.objects.filter(user=user)
        return sum(basket.quantity for basket in baskets)

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт {self.product.name} | Количество {self.quantity}'

    def de_json(self):
        basket_item = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum()),
        }
        return basket_item

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"