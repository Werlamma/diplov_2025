from django.urls import path
from .views import OrderCreateView, SuccessTemplateView, CanceledTemplateView, OrderDetailView

app_name = 'orders'

urlpatterns = [
    path('order/', OrderCreateView.as_view(), name='order_create'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order_list'),
    path('order-success/', SuccessTemplateView.as_view(), name='order_success'),
    path('order-canceled/', CanceledTemplateView.as_view(), name='order_canceled'),
]
