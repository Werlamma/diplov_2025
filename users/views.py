from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView, UpdateView, View
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import views as auth_views
from .forms import (UserLoginForm, UserRegisterForm, UserProfileForm, CustomPasswordResetForm,
                    CustomSetPasswordForm)
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from vacancy.models import VacancyApplication
from django.contrib.auth import logout
from django.contrib import messages
from django.http import JsonResponse
from orders.models import Order

class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user:
            auth_login(self.request, user)
            messages.success(self.request, 'Вы успешно вошли в систему!')

            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({"success": True})

            return super().form_valid(form)
        else:
            # Добавляем ошибку в форму
            form.add_error(None, "Неверный логин или пароль")
            return self.form_invalid(form)

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            errors = {field: [error for error in error_list] for field, error_list in form.errors.items()}
            if form.non_field_errors():
                errors["password"] = form.non_field_errors()
            return JsonResponse({"success": False, "errors": errors})
        return super().form_invalid(form)


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'Вы успешно зарегистрировались!')

        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({"success": True})

        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({"success": False, "errors": form.errors}, status=400)

        return super().form_invalid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    form_class = UserProfileForm  # Форма для редактирования
    template_name = 'users/profile.html'  # Шаблон для отображения
    success_url = reverse_lazy('users:profile')  # URL для перенаправления после успешного редактирования

    def get_object(self, queryset=None):
        # Возвращаем текущего авторизованного пользователя
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['user'] = user

        context['orders'] = Order.objects.filter(initiator=user).order_by('-created_at')

        for order in context['orders']:
            order.status_display = order.get_status_display()

        context['applications'] = VacancyApplication.objects.filter(user=user)

        return context

    def form_valid(self, form):
        form.save()
        # Возвращаем JSON-ответ для AJAX
        return JsonResponse({
            'success': True,
            'message': 'Данные успешно обновлены!',
        })

    def form_invalid(self, form):
        # Возвращаем JSON-ответ с ошибками
        return JsonResponse({
            'success': False,
            'errors': form.errors,
        }, status=400)


class CustomLogoutView(View):
    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        # Выход из системы
        logout(request)
        messages.success(request, 'Вы успешно вышли из системы!')
        return redirect('main:home')


class CustomPasswordResetView(auth_views.PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_url = '/users/password_reset/done/'

    def form_valid(self, form):
        response = super().form_valid(form)

        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({"success": True})

        return response

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({"success": False, "errors": form.errors}, status=400)

        return super().form_invalid(form)


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    form_class = CustomSetPasswordForm  # Используем кастомную форму
    template_name = 'users/password_reset_confirm.html'  # Ваш шаблон
    success_url = '/users/reset/done/'  # URL после успешного сброса

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uidb64'] = self.kwargs.get('uidb64')
        context['token'] = self.kwargs.get('token')
        return context

    def form_valid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            super().form_valid(form)  # Выполняем стандартную обработку
            return JsonResponse({"success": True})

        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({"success": False, "errors": form.errors}, status=400)

        return super().form_invalid(form)


