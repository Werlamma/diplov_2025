from django.contrib import admin
from django.utils.html import format_html
from .models import Vacancy, Tag, VacancyApplication


admin.site.register(VacancyApplication)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Отображаемые поля в списке тегов
    search_fields = ('name',)  # Поля для поиска
    list_per_page = 20  # Количество тегов на странице


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'formatted_salary_display',
        'experience',
        'employment_type',
        'schedule',
        'qualification',
        'tags_display',
    )  # Отображаемые поля в списке вакансий
    list_filter = (
        'experience',
        'employment_type',
        'schedule',
        'qualification',
        'salary',
    )  # Фильтры в правой части интерфейса
    search_fields = ('title', 'description')  # Поля для поиска
    filter_horizontal = ('tags',)  # Удобный виджет для выбора тегов
    list_per_page = 20  # Количество вакансий на странице

    def formatted_salary_display(self, obj):
        """Отображает отформатированную зарплату в списке вакансий."""
        return obj.formatted_salary()

    formatted_salary_display.short_description = "Зарплата"  # Заголовок колонки

    def tags_display(self, obj):
        """Отображает теги в виде строки через запятую."""
        return ", ".join([tag.name for tag in obj.tags.all()])

    tags_display.short_description = "Теги"  # Заголовок колонки

    # Настройка формы редактирования вакансии
    fieldsets = (
        (None, {
            'fields': ('title', 'description')
        }),
        ('Зарплата', {
            'fields': ('salary', 'salary_display')
        }),
        ('Детали', {
            'fields': ('experience', 'employment_type', 'schedule', 'qualification')
        }),
        ('Теги', {
            'fields': ('tags',)
        }),
    )
