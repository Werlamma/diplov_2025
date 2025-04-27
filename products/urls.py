from django.urls import path
from .views import ProductsView, ProductDetailView, BasketView, AddToBasketView, RemoveFromBasketView, UpdateBasketView

app_name = 'products'

urlpatterns = [
    path('', ProductsView.as_view(), name='products'),
    path('basket/', BasketView.as_view(), name='basket'),
    path('basket/update/<slug:slug>/', UpdateBasketView.as_view(), name='update_basket'),
    path("basket/remove/<slug:product_slug>/", RemoveFromBasketView.as_view(), name="remove_from_basket"),
    path('products/<slug:product_slug>/add/', AddToBasketView.as_view(), name='add_to_basket'),
    path('<slug:product_slug>/', ProductDetailView.as_view(), name='product_detail'),

]
