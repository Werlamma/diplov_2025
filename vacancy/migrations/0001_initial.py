# Generated by Django 5.1.7 on 2025-03-24 10:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название тега')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название вакансии')),
                ('description', models.TextField(verbose_name='Описание')),
                ('salary_display', models.CharField(default='', max_length=100, verbose_name='Зарплата (текст для отображения)')),
                ('salary', models.CharField(choices=[('under_30k', 'До 30 000 ₽'), ('30k_to_50k', 'От 30 000 до 50 000 ₽'), ('over_50k', 'От 50 000 ₽')], max_length=100, verbose_name='Зарплата')),
                ('experience', models.CharField(choices=[('no_experience', 'Без опыта'), ('up_to_year', 'До года'), ('from_1_year', 'От 1 года'), ('more_than_2_years', 'Более 2 лет')], max_length=50, verbose_name='Опыт')),
                ('employment_type', models.CharField(choices=[('full', 'Полная'), ('partial', 'Частичная')], max_length=50, verbose_name='Тип занятости')),
                ('schedule', models.CharField(choices=[('removable', 'Сменный'), ('complete', 'Полный'), ('flexible', 'Гибкий')], max_length=50, verbose_name='График работы')),
                ('qualification', models.CharField(choices=[('elementary', 'Начальный'), ('average', 'Средний'), ('high', 'Высокий')], max_length=50, verbose_name='Уровень квалификации')),
                ('tags', models.ManyToManyField(related_name='vacancies', to='vacancy.tag', verbose_name='Теги')),
            ],
            options={
                'verbose_name': 'Вакансия',
                'verbose_name_plural': 'Вакансии',
            },
        ),
        migrations.CreateModel(
            name='VacancyApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=100, verbose_name='Фамилия')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('birthdate', models.DateField(verbose_name='Дата рождения')),
                ('education_level', models.CharField(max_length=100, verbose_name='Уровень образования')),
                ('specialty', models.CharField(max_length=100, verbose_name='Специальность')),
                ('additional_education', models.TextField(verbose_name='Дополнительное образование')),
                ('additional_info', models.TextField(verbose_name='Дополнительная информация')),
                ('status', models.CharField(choices=[('created', 'Создана'), ('in_review', 'В рассмотрении'), ('accepted', 'Принята'), ('rejected', 'Отклонена')], default='created', max_length=20, verbose_name='Статус')),
                ('rejection_reason', models.TextField(blank=True, null=True, verbose_name='Причина отказа')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата подачи заявки')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to=settings.AUTH_USER_MODEL)),
                ('vacancy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='vacancy.vacancy')),
            ],
            options={
                'verbose_name': 'Заявка на вакансию',
                'verbose_name_plural': 'Заявки на вакансии',
            },
        ),
    ]
