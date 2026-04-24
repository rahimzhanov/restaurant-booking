from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('cancelled', 'Отмена'),
        ('completed', 'Завершено'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name='Клиент'
    )
    table = models.ForeignKey(
        'tables.Table',
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name='Столик'
    )
    date = models.DateField('Дата')
    time = models.TimeField('Время')
    duration = models.IntegerField('Длительность (часы)', default=2)
    guests = models.IntegerField('Количество гостей')
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    comment = models.TextField('Комментарий', blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
        ordering = ['-date', '-time']
        constraints = [
            # Уникальность: один столик не может быть забронирован на одно время
            models.UniqueConstraint(
                fields=['table', 'date', 'time'],
                name='unique_booking'
            )
        ]

    def __str__(self):
        return f'Бронь №{self.id}: {self.user.email} - Столик №{self.table.number} на {self.date} {self.time}'

    def clean(self):
        # Проверка, что дата бронирования не в прошлом
        booking_datetime = timezone.make_aware(
            timezone.datetime.combine(self.date, self.time)
        )
        if booking_datetime < timezone.now():
            raise ValidationError('Нельзя забронировать на прошедшее время')

        # Проверка количества гостей
        if self.guests > self.table.seats:
            raise ValidationError(f'Столик вмещает только {self.table.seats} гостей')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)