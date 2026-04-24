from django.db import models


class Table(models.Model):
    number = models.IntegerField('Номер столика', unique=True)
    seats = models.IntegerField('Количество мест')
    location = models.CharField('Расположение', max_length=100, blank=True,
                                help_text='У окна, в центре, VIP-зона и т.д.')
    is_active = models.BooleanField('Активен', default=True)
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Столик'
        verbose_name_plural = 'Столики'
        ordering = ['number']

    def __str__(self):
        return f'Столик №{self.number} ({self.seats} мест)'

    @property
    def is_available(self):
        """Будет использоваться для проверки доступности"""
        return self.is_active