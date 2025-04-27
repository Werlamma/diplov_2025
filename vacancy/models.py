from django.db import models
from users.models import User


class Vacancy(models.Model):
    EXPERIENCE_CHOICES = [
        ('no_experience', 'Без опыта'),
        ('up_to_year', 'До года'),
        ('from_1_year', 'От 1 года'),
        ('more_than_2_years', 'Более 2 лет'),
    ]

    EMPLOYMENT_TYPE_CHOICES = [
        ('full', 'Полная'),
        ('partial', 'Частичная'),
    ]

    SCHEDULE_CHOICES = [
        ('removable', 'Сменный'),
        ('complete', 'Полный'),
        ('flexible', 'Гибкий'),
    ]

    QUALIFICATION_CHOICES = [
        ('elementary', 'Начальный'),
        ('average', 'Средний'),
        ('high', 'Высокий'),
    ]

    SALARY_CHOICES = [
        ('under_30k', 'До 30 000 ₽'),
        ('30k_to_50k', 'От 30 000 до 50 000 ₽'),
        ('over_50k', 'От 50 000 ₽'),
    ]

    title = models.CharField(max_length=255, verbose_name="Название вакансии")
    description = models.TextField(verbose_name="Описание")
    salary_display = models.CharField(max_length=100, default='', verbose_name="Зарплата (текст для отображения)")
    salary = models.CharField(max_length=100, verbose_name="Зарплата", choices=SALARY_CHOICES)
    experience = models.CharField(max_length=50, verbose_name="Опыт", choices=EXPERIENCE_CHOICES)
    employment_type = models.CharField(max_length=50, verbose_name="Тип занятости", choices=EMPLOYMENT_TYPE_CHOICES)
    schedule = models.CharField(max_length=50, verbose_name="График работы", choices=SCHEDULE_CHOICES)
    qualification = models.CharField(max_length=50, verbose_name="Уровень квалификации", choices=QUALIFICATION_CHOICES)
    tags = models.ManyToManyField('Tag', verbose_name="Теги", related_name='vacancies')

    def formatted_salary(self):
        """Возвращает отформатированную зарплату."""
        salary = self.salary_display
        if salary.isdigit():  # Если зарплата — это число
            return f"От {int(salary):,} ₽".replace(",", " ")  # Форматируем с пробелами
        elif "-" in salary:  # Если зарплата в формате "30000-50000"
            return salary.replace("-", " – ") + " ₽"  # Добавляем пробелы и символ рубля
        elif salary.lower() == "договорная":  # Если зарплата "Договорная"
            return "Зарплата по договоренности"
        return salary  # Возвращаем как есть

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название тега")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class VacancyApplication(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('in_review', 'В рассмотрении'),
        ('accepted', 'Принята'),
        ('rejected', 'Отклонена'),  # Добавляем статус "Отклонена"
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    birthdate = models.DateField(verbose_name="Дата рождения")
    education_level = models.CharField(max_length=100, verbose_name="Уровень образования")
    specialty = models.CharField(max_length=100, verbose_name="Специальность")
    additional_education = models.TextField(verbose_name="Дополнительное образование")
    additional_info = models.TextField(verbose_name="Дополнительная информация")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created', verbose_name="Статус")
    rejection_reason = models.TextField(blank=True, null=True, verbose_name="Причина отказа")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подачи заявки")

    def __str__(self):
        return f"Заявка #{self.id} от {self.user.username}"

    class Meta:
        verbose_name = "Заявка на вакансию"
        verbose_name_plural = "Заявки на вакансии"
