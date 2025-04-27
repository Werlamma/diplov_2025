from django.db import models
from users.models import User
from products.models import Basket


class Order(models.Model):
    CREATED = 0
    CONFIRMED = 1
    PLANNING = 2
    IN_PRODUCTION = 3
    QUALITY_CONTROL = 4
    READY_FOR_SHIPMENT = 5
    SENT_TO_DELIVERY = 6
    DELIVERED = 7
    COMPLETED = 8
    CANCELLED = 9

    STATUS_CHOICES = [
        (CREATED, 'Новый'),
        (CONFIRMED, 'Подтверждён'),
        (PLANNING, 'В планировании'),
        (IN_PRODUCTION, 'В производстве'),
        (QUALITY_CONTROL, 'Контроль качества (ОТК)'),
        (READY_FOR_SHIPMENT, 'Готов к отгрузке'),
        (SENT_TO_DELIVERY, 'Передан в доставку'),
        (DELIVERED, 'Доставлен'),
        (COMPLETED, 'Завершён'),
        (CANCELLED, 'Отменён'),
    ]

    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    email = models.EmailField(max_length=256, verbose_name='Почта')
    phone_number = models.CharField(max_length=50, verbose_name='Номер телефона')
    address = models.CharField(max_length=256, verbose_name='Адрес доставки')
    basket_history = models.JSONField(default=dict, verbose_name='История корзины')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Пользователь')
    rejection_reason = models.TextField(blank=True, null=True, verbose_name="Причина отказа")
    status = models.SmallIntegerField(default=CREATED, choices=STATUS_CHOICES, verbose_name='Статус')

    def __str__(self):
        return f'Заказ {self.id} {self.first_name} {self.last_name}'

    def update_after_payment(self):
        baskets = Basket.objects.filter(user=self.initiator)
        self.status = self.CONFIRMED
        self.basket_history = {
            'purchased_items': [basket.de_json() for basket in baskets],
            'total_sum': float(Basket.total_sum(self.initiator)),
        }
        baskets.delete()
        self.save()

