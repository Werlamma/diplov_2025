from django import forms
from .models import VacancyApplication
from django.core.validators import RegexValidator

cyrillic_validator = RegexValidator(
    regex=r'^[А-Яа-яЁё\s\-]+$',
    message='Разрешены только кириллические буквы, пробелы и тире.'
)


class VacancyApplicationForm(forms.ModelForm):
    first_name = forms.CharField(
        validators=[cyrillic_validator],
        widget=forms.TextInput(attrs={'class': 'bid__input', 'placeholder': 'Введите ваше Имя'})
    )
    last_name = forms.CharField(
        validators=[cyrillic_validator],
        widget=forms.TextInput(attrs={'class': 'bid__input', 'placeholder': 'Введите вашу Фамилию'})
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'bid__input', 'placeholder': 'Введите свой телефон'})
    )
    birthdate = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'bid__input', 'placeholder': 'Введите свою дату рождения'})
    )
    education_level = forms.CharField(
        validators=[cyrillic_validator],
        widget=forms.TextInput(attrs={'class': 'bid__input', 'placeholder': 'Введите ваш уровень образования'})
    )
    specialty = forms.CharField(
        validators=[cyrillic_validator],
        widget=forms.TextInput(attrs={'class': 'bid__input', 'placeholder': 'Введите название специальности'})
    )
    additional_education = forms.CharField(
        validators=[cyrillic_validator],
        widget=forms.Textarea(attrs={
            'class': 'bid__textarea', 'placeholder': 'Укажите какое доп. образование у вас есть'}),
        required=False
    )
    additional_info = forms.CharField(
        validators=[cyrillic_validator],
        widget=forms.Textarea(attrs={
            'class': 'bid__textarea', 'placeholder': 'Введите информацию, которую мы должны знать о вас'}),
        required=False
    )

    class Meta:
        model = VacancyApplication
        fields = ('first_name', 'last_name', 'phone', 'birthdate', 'education_level', 'specialty',
                  'additional_education', 'additional_info')
