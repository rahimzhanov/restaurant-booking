from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm


class RegisterView(CreateView):
    """
    Регистрация нового пользователя.

    CreateView — это готовый CBV для создания объектов:
    1. GET-запрос: показывает пустую форму
    2. POST-запрос: проверяет данные и создаёт пользователя
    """
    form_class = CustomUserCreationForm  # Какую форму использовать
    template_name = 'users/register.html'  # Какой шаблон показывать
    success_url = reverse_lazy('bookings:profile')  # Куда перенаправить после успеха

    def form_valid(self, form):
        """
        Вызывается, когда форма прошла валидацию.
        Переопределяем, чтобы:
        1. Автоматически войти после регистрации
        2. Показать приветственное сообщение
        """
        # Сохраняем пользователя (вызывает form.save())
        response = super().form_valid(form)

        # Автоматически входим под созданным пользователем
        login(self.request, self.object)

        # Показываем зелёное сообщение об успехе
        messages.success(
            self.request,
            f'Добро пожаловать, {self.object.first_name}! Ваш аккаунт успешно создан.'
        )

        return response

    def dispatch(self, request, *args, **kwargs):
        """
        dispatch — первый метод, который вызывается при любом запросе.
        Если пользователь уже авторизован, перенаправляем в профиль.
        """
        if request.user.is_authenticated:
            return redirect('bookings:profile')
        return super().dispatch(request, *args, **kwargs)


class CustomLoginView(LoginView):
    """
    Вход в систему.

    LoginView — стандартный CBV Django для аутентификации:
    1. GET: показывает форму входа
    2. POST: проверяет email/пароль и создаёт сессию
    """
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True  # Если уже вошёл — сразу в профиль

    def form_valid(self, form):
        """Показываем сообщение при успешном входе"""
        messages.success(self.request, f'С возвращением, {form.get_user().first_name}!')
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, TemplateView):
    """
    Личный кабинет пользователя.

    LoginRequiredMixin — примесь, которая проверяет авторизацию.
    Если пользователь не вошёл — перенаправляет на страницу входа.
    TemplateView — просто показывает шаблон без дополнительной логики.
    """
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        """
        Добавляем дополнительные данные в контекст шаблона.
        Здесь мы можем передать бронирования пользователя.
        """
        context = super().get_context_data(**kwargs)
        # Пока передаём пустой список, на Этапе 3 добавим бронирования
        context['bookings'] = []
        return context