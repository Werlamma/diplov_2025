from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, View
from .models import Category, Product, Basket
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect


class ProductsView(ListView):
    model = Category
    template_name = 'products/products.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем все продукты в контекст, если нужно
        context['products'] = Product.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product.html'
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'


class BasketView(LoginRequiredMixin, TemplateView):
    template_name = 'products/basket.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            # Получаем все товары в корзине пользователя
            baskets = Basket.objects.filter(user=user)
            context['baskets'] = baskets
            context['total_sum'] = Basket.total_sum(user)
            context['total_quantity'] = Basket.total_quantity(user)
        else:
            # Если пользователь не авторизован, возвращаем пустые значения
            context['baskets'] = []
            context['total_sum'] = 0
            context['total_quantity'] = 0

        return context


class AddToBasketView(LoginRequiredMixin, View):
    def post(self, request, product_slug):
        product = get_object_or_404(Product, slug=product_slug)
        basket_item, created = Basket.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': 1}
        )

        if not created:
            basket_item.quantity += 1
            basket_item.save()

        return JsonResponse({
            'success': True,
            'quantity': basket_item.quantity,
            'message': "Товар успешно добавлен в корзину!"
        })


class RemoveFromBasketView(LoginRequiredMixin, View):
    def post(self, request, product_slug):
        product = get_object_or_404(Product, slug=product_slug)
        basket_item = Basket.objects.filter(user=request.user, product=product).first()

        if basket_item:
            basket_item.delete()
            total_quantity = Basket.objects.filter(user=request.user).count()
            total_sum = sum(item.product.price * item.quantity for item in Basket.objects.filter(user=request.user))
            message = "Товар удален из корзины!"
        else:
            message = "Товар не найден в корзине!"

        return JsonResponse({
            "success": True,
            "message": message,
            "total_quantity": total_quantity,
            "total_sum": total_sum
        })


@method_decorator(csrf_protect, name='dispatch')
class UpdateBasketView(LoginRequiredMixin, View):
    def post(self, request, slug):
        try:
            data = json.loads(request.body)
            action = data.get("action")

            basket_item = Basket.objects.filter(user=request.user, product__slug=slug).first()
            if not basket_item:
                return JsonResponse({"success": False, "error": "Товар не найден"}, status=400)

            if action == "increase":
                basket_item.quantity += 1
            elif action == "decrease" and basket_item.quantity > 1:
                basket_item.quantity -= 1

            basket_item.save()

            return JsonResponse({
                "success": True,
                "new_quantity": basket_item.quantity,
                "new_sum": basket_item.sum(),
                "total_sum": Basket.total_sum(request.user),
                "total_quantity": Basket.total_quantity(request.user)
            })

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Ошибка в JSON-данных"}, status=400)

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)



