from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    """
    Форма регистрации нового пользователя.

    Наследуемся от UserCreationForm, чтобы:
    1. Получить готовую логику валидации паролей
    2. Получить метод save() для создания пользователя
    3. Добавить свои поля (email, phone, имя)
    """

    first_name = forms.CharField(
        label="Имя",
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Введите ваше имя"}
        ),
    )

    phone = forms.CharField(
        label="Телефон",
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "+7 (999) 123-45-67"}
        ),
    )

    class Meta:
        model = User
        fields = ["email", "first_name", "phone", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        """Добавляем CSS-классы и плейсхолдеры ко всем полям"""
        super().__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "example@email.com"}
        )
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Придумайте пароль"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Повторите пароль"}
        )

    def save(self, commit=True):
        """
        Переопределяем метод save, чтобы автоматически
        генерировать username из email.

        Это решает проблему уникальности username:
        - Берём часть email до @
        - Если такой username уже существует, добавляем цифры
        """
        user = super().save(commit=False)

        # Генерируем username из email (часть до @)
        base_username = self.cleaned_data["email"].split("@")[0]
        username = base_username

        # Если такой username уже есть, добавляем номер
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user.username = username

        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """
    Форма входа в систему.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите email"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите пароль"}
        )
