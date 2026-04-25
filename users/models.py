from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Кастомная модель пользователя для ресторана.

    Наследуемся от AbstractUser, чтобы:
    1. Сохранить всю стандартную функциональность Django (пароли, группы, разрешения)
    2. Добавить свои поля (роль, телефон)
    3. Использовать email как основной идентификатор вместо username
    """

    # Кортеж с вариантами ролей: (значение_в_БД, человекочитаемое_название)
    ROLE_CHOICES = [
        ('client', 'Клиент'),  # Обычный пользователь, может бронировать
        ('admin', 'Администратор'),  # Управляет бронью, столиками
    ]

    # Email делаем уникальным - теперь это основной способ входа
    # unique=True гарантирует, что не будет двух пользователей с одинаковым email
    email = models.EmailField('Email', unique=True)

    # Телефон - необязательное поле, max_length=20 для международных номеров
    phone = models.CharField('Телефон', max_length=20, blank=True)

    # Роль с выбором из ROLE_CHOICES, по умолчанию - клиент
    # default='client' означает, что при регистрации все становятся клиентами
    role = models.CharField('Роль', max_length=10, choices=ROLE_CHOICES, default='client')

    # Указываем, что для аутентификации будет использоваться email, а не username
    USERNAME_FIELD = 'email'

    # Поля, которые обязательно нужно заполнить при создании суперпользователя
    # Команда createsuperuser запросит email и username
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'  # Название в единственном числе
        verbose_name_plural = 'Пользователи'  # Название во множественном числе

    def __str__(self):
        """Как объект будет отображаться в админке и при печати"""
        return f'{self.email} ({self.get_role_display()})'

    @property
    def is_admin_staff(self):
        """
        Проверка, является ли пользователь администратором ресторана.
        Свойство @property позволяет вызывать без скобок: user.is_admin_staff
        """
        return self.role == 'admin' or self.is_staff