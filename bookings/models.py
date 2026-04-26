from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime


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
            models.UniqueConstraint(
                fields=['table', 'date', 'time'],
                name='unique_booking'
            )
        ]

    def __str__(self):
        return f'Бронь №{self.id}: {self.user.email} - Столик №{self.table.number} на {self.date} {self.time}'

    def clean(self):
        # Проверка, что дата бронирования не в прошлом
        booking_start = timezone.make_aware(
            datetime.datetime.combine(self.date, self.time)
        )
        if booking_start < timezone.now():
            raise ValidationError('Нельзя забронировать столик на прошедшее время.')

        # Проверка количества гостей
        if self.guests > self.table.seats:
            raise ValidationError(
                f'Столик №{self.table.number} вмещает только {self.table.seats} гостей. '
                f'Вы указали {self.guests}.'
            )

        # Проверка пересечения с другими бронями
        booking_end = booking_start + datetime.timedelta(hours=self.duration)

        # Ищем все брони этого столика на эту дату (кроме текущей, если редактируем)
        conflicting_bookings = Booking.objects.filter(
            table=self.table,
            date=self.date,
            status__in=['pending', 'confirmed']  # Активные брони
        )

        if self.pk:  # Если это редактирование существующей брони
            conflicting_bookings = conflicting_bookings.exclude(pk=self.pk)

        for other_booking in conflicting_bookings:
            other_start = timezone.make_aware(
                datetime.datetime.combine(other_booking.date, other_booking.time)
            )
            other_end = other_start + datetime.timedelta(hours=other_booking.duration)

            # Проверяем пересечение интервалов
            if booking_start < other_end and booking_end > other_start:
                raise ValidationError(
                    f'Столик №{self.table.number} уже забронирован '
                    f'на {other_booking.date.strftime("%d.%m.%Y")} '
                    f'с {other_booking.time.strftime("%H:%M")} '
                    f'на {other_booking.duration} ч. '
                    f'Выберите другое время.'
                )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)