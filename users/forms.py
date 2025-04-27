from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm, UserChangeForm, PasswordResetForm,
                                       SetPasswordForm)
from users.models import User
from django.core.exceptions import ValidationError
import re


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'login__input', 'placeholder': 'Введите ваш логин', 'autocomplete': 'username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'login__input', 'placeholder': 'Введите ваш пароль', 'autocomplete': 'current-password'
    }))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'registration__input', 'placeholder': 'Введите ваше Имя'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'registration__input', 'placeholder': 'Введите вашу Фамилию'
    }))
    patronymic = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'registration__input', 'placeholder': 'Введите ваше Отчество'
    }), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'registration__input', 'placeholder': 'Введите ваш логин', 'autocomplete': 'username'
    }))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'registration__input', 'placeholder': 'Введите ваш номер'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'registration__input', 'placeholder': 'Введите вашу Почту', 'autocomplete': 'email'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'registration__input', 'placeholder': 'Введите ваш Пароль', 'autocomplete': 'new-password'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'registration__input', 'placeholder': 'Подтвердите ваш Пароль', 'autocomplete': 'new-password'
    }))

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not re.match(r'^[а-яА-ЯёЁ\s-]+$', first_name):
            raise ValidationError('Имя должно содержать только кириллицу, пробелы и тире.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not re.match(r'^[а-яА-ЯёЁ\s-]+$', last_name):
            raise ValidationError('Фамилия должна содержать только кириллицу, пробелы и тире.')
        return last_name

    def clean_patronymic(self):
        patronymic = self.cleaned_data.get('patronymic')
        if patronymic and not re.match(r'^[а-яА-ЯёЁ\s-]+$', patronymic):
            raise ValidationError('Отчество должно содержать только кириллицу, пробелы и тире.')
        return patronymic

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с такой почтой уже существует.')
        return email

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'patronymic', 'username', 'phone_number', 'email',
                  'password1', 'password2')


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'profile-content__form-input'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'profile-content__form-input'
    }))
    patronymic = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'profile-content__form-input'
    }), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'profile-content__form-input', 'readonly': True
    }))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'profile-content__form-input'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'profile-content__form-input', 'autocomplete': 'email', 'readonly': True
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'patronymic', 'username', 'phone_number', 'email')


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'forgot-password__input',
            'placeholder': 'Введите ваш email',
            'autocomplete': 'email'
        })
    )


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'forgot-password__input',
            'placeholder': 'Новый пароль',
            'autocomplete': 'new-password'
        })
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'forgot-password__input',
            'placeholder': 'Подтвердите пароль',
            'autocomplete': 'new-password'
        })
    )
