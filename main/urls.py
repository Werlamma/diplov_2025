from django.urls import path
from .views import HomePageView, AboutPageView, ContactsPageView, PartnersPageView, PolicyPageView

app_name = 'main'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('contacts/', ContactsPageView.as_view(), name='contacts'),
    path('partners/', PartnersPageView.as_view(), name='partners'),
    path('policy/', PolicyPageView.as_view(), name='policy')
]
