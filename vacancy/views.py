from django.views.generic import ListView, DetailView
from .models import Vacancy
from django.http import JsonResponse
import json
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import VacancyApplicationForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import VacancyApplication
from django.views import View
from django.contrib import messages


class VacancyListView(ListView):
    model = Vacancy
    template_name = 'vacancy/vacancy.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
        queryset = super().get_queryset()

        # Фильтрация по опыту
        experience = self.request.GET.getlist('experience')
        if experience:
            queryset = queryset.filter(experience__in=experience)

        # Фильтрация по типу занятости
        employment_type = self.request.GET.getlist('employment_type')
        if employment_type:
            queryset = queryset.filter(employment_type__in=employment_type)

        # Фильтрация по графику работы
        schedule = self.request.GET.getlist('schedule')
        if schedule:
            queryset = queryset.filter(schedule__in=schedule)

        # Фильтрация по уровню квалификации
        qualification = self.request.GET.getlist('qualification')
        if qualification:
            queryset = queryset.filter(qualification__in=qualification)

        # Фильтрация по зарплате
        salary = self.request.GET.getlist('salary')
        if salary:
            queryset = queryset.filter(salary__in=salary)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем все возможные значения для фильтров в контекст
        context['experience_choices'] = Vacancy.EXPERIENCE_CHOICES
        context['employment_type_choices'] = Vacancy.EMPLOYMENT_TYPE_CHOICES
        context['schedule_choices'] = Vacancy.SCHEDULE_CHOICES
        context['qualification_choices'] = Vacancy.QUALIFICATION_CHOICES
        context['salary_choices'] = Vacancy.SALARY_CHOICES
        return context


class VacancyDetailView(DetailView):
    model = Vacancy
    template_name = 'vacancy/vacancy_detail.html'
    context_object_name = 'vacancy'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = VacancyApplicationForm()
        return context

    def post(self, request, *args, **kwargs):
        # Проверяем, авторизован ли пользователь
        if not request.user.is_authenticated:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({"success": False, "login_required": True, "redirect_url": reverse_lazy('users:login')}, status=403)
            return redirect(reverse_lazy('users:login'))

        self.object = self.get_object()
        vacancy = self.get_object()
        form = VacancyApplicationForm(request.POST)

        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.vacancy = vacancy
            application.save()
            messages.success(request, 'Ваша заявка успешно отправлена!')

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({"success": True})

            return redirect(reverse_lazy('users:profile'))

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({"success": False, "errors": form.errors}, status=400)

        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)


class RevokeApplicationView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        application = get_object_or_404(VacancyApplication, pk=pk)

        # Убеждаемся, что заявка принадлежит пользователю
        if application.user != request.user:
            return JsonResponse({'success': False, 'error': 'Вы не можете удалить эту заявку!'}, status=403)

        application.delete()
        return JsonResponse({
            'success': True,
            'message': 'Ваша заявка успешно отозвана!'
        })


class ApplicationDetailView(LoginRequiredMixin, DetailView):
    model = VacancyApplication
    template_name = "vacancy/vacancy_profile_detail.html"
    context_object_name = "application"

    def get_object(self, queryset=None):
        return get_object_or_404(VacancyApplication, pk=self.kwargs.get("pk"))


def filter_vacancies(request):
    if request.method == 'POST':
        filters = json.loads(request.body)
        queryset = Vacancy.objects.all()

        # Применяем фильтры
        if filters.get('experience'):
            queryset = queryset.filter(experience__in=filters['experience'])
        if filters.get('employment_type'):
            queryset = queryset.filter(employment_type__in=filters['employment_type'])
        if filters.get('schedule'):
            queryset = queryset.filter(schedule__in=filters['schedule'])
        if filters.get('qualification'):
            queryset = queryset.filter(qualification__in=filters['qualification'])
        if filters.get('salary'):
            queryset = queryset.filter(salary__in=filters['salary'])

        # Преобразуем данные в JSON
        data = []
        for vacancy in queryset:
            data.append({
                'id': vacancy.id,
                'title': vacancy.title,
                'description': vacancy.description,
                'salary': vacancy.salary,
                'salary_display': vacancy.formatted_salary(),  # Используем метод из модели
                'tags': [{'name': tag.name} for tag in vacancy.tags.all()],
            })

        return JsonResponse(data, safe=False)

