from django import forms
from orders.models import Order
from django.core.validators import RegexValidator

cyrillic_validator = RegexValidator(
    regex=r'^[А-Яа-яЁё\s\-]+$',
    message='Разрешены только кириллические буквы, пробелы и тире.'
)

address_validator = RegexValidator(
    regex=r'^[А-Яа-яЁё0-9\s\-\.,]+$',
    message='Разрешены только кириллические буквы, пробелы и тире.'
)


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(
        validators=[cyrillic_validator],
        widget=forms.TextInput(attrs={'class': 'order-form__input', 'placeholder': 'Введите ваше Имя'})
    )
    last_name = forms.CharField(
        validators=[cyrillic_validator],
        widget=forms.TextInput(attrs={'class': 'order-form__input', 'placeholder': 'Введите вашу Фамилию'})
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'order-form__input', 'placeholder': 'Введите адрес электронной почты', 'autocomplete': 'email'
    }))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'order-form__input', 'placeholder': 'Введите ваш номер'
    }))
    address = forms.CharField(
        validators=[address_validator],
        widget=forms.TextInput(attrs={'class': 'order-form__input', 'placeholder': 'Введите адрес доставки'})
    )

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address']
