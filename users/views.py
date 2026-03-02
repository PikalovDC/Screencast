from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.views.generic import CreateView, FormView, View
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserRegistrationForm, UserLoginForm
from .models import User

class UserRegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        """Если форма валидна, отправляем письмо и логиним пользователя"""
        response = super().form_valid(form)

        # Отправка приветственного письма
        send_mail(
            subject='Добро пожаловать в Skystore!',
            message=f'Здравствуйте, {self.object.email}!\n\n'
                    f'Спасибо за регистрацию в нашем магазине.\n\n'
                    f'С уважением,\n'
                    f'Команда Skystore',
            from_email='noreply@skystore.com',
            recipient_list=[self.object.email],
            fail_silently=True,
        )

        # Автоматический вход после регистрации
        login(self.request, self.object)
        messages.success(self.request, 'Регистрация прошла успешно!')

        return response

class UserLoginView(LoginView):
    """Авторизация пользователя"""
    form_class = UserLoginForm
    template_name = 'users/login.html'
    next_page = reverse_lazy('catalog:home')

    def form_valid(self, form):
        """Если форма валидна, добавляем сообщение"""
        response = super().form_valid(form)
        messages.success(self.request, f'С возвращением, {self.request.user.email}!')
        return response

    def form_invalid(self, form):
        """Если форма невалидна, добавляем сообщение об ошибке"""
        messages.error(self.request, 'Неверный email или пароль')
        return super().form_invalid(form)


class UserLogoutView(LogoutView):
    """Выход из системы"""
    next_page = reverse_lazy('catalog:home')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'Вы вышли из системы')
        return super().dispatch(request, *args, **kwargs)
