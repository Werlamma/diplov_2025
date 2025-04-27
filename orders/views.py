import stripe
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from .forms import OrderForm
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from products.models import Basket
from orders.models import Order
from django.contrib.auth.mixins import LoginRequiredMixin

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/order-success.html'


class CanceledTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/order-cancel.html'


class OrderDetailView(LoginRequiredMixin, DetailView):
    template_name = 'orders/order_detail.html'
    model = Order
    context_object_name = "order"

    def get_object(self, queryset=None):
        return get_object_or_404(Order, pk=self.kwargs.get("pk"))


class OrderCreateView(LoginRequiredMixin, CreateView):
    form_class = OrderForm
    template_name = 'orders/order_form.html'

    def form_valid(self, form):
        order = form.save(commit=False)
        order.initiator = self.request.user
        order.save()
        self.object = order
        baskets = Basket.objects.filter(user=self.request.user)
        line_items = []
        for basket in baskets:
            item = {
                'price': basket.product.stripe_product_price_id,
                'quantity': basket.quantity,
            }
            line_items.append(item)

        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url=f"{settings.DOMAIN_NAME}{reverse('orders:order_success')}",
            cancel_url=f"{settings.DOMAIN_NAME}{reverse('orders:order_canceled')}",
        )
        return JsonResponse({
            "success": True,
            "redirect_url": checkout_session.url
        })

    def form_invalid(self, form):
        return JsonResponse({
            "success": False,
            "errors": form.errors
        }, status=400)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event['type'] in ['checkout.session.completed', 'checkout.session.async_payment_succeeded']:
        fulfill_checkout(event['data']['object'])  # Передаём объект, а не id

    return HttpResponse(status=200)


def fulfill_checkout(session):
    order_id = session.get('metadata', {}).get('order_id')  # Безопасное извлечение

    if not order_id:
        return  # Не нашли order_id, не можем обработать заказ

    try:
        order = Order.objects.get(id=int(order_id))
    except Order.DoesNotExist:
        return  # Заказ не найден

    order.update_after_payment()

