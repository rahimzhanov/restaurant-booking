from django.db import models


class SiteContent(models.Model):
    """
    Модель для хранения редактируемого контента сайта.
    Администратор может менять текст через админку без правки кода.
    """
    SECTION_CHOICES = [
        ('home_about', 'Главная: О ресторане'),
        ('home_services', 'Главная: Услуги'),
        ('home_contact', 'Главная: Контакты'),
        ('about_history', 'О ресторане: История'),
        ('about_mission', 'О ресторане: Миссия и ценности'),
        ('about_team', 'О ресторане: Команда'),
        ('footer', 'Подвал сайта'),
    ]

    section = models.CharField(
        'Раздел',
        max_length=50,
        choices=SECTION_CHOICES,
        unique=True,
        help_text='Выберите раздел сайта для редактирования'
    )
    title = models.CharField('Заголовок', max_length=200)
    content = models.TextField('Содержание', blank=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Контент сайта'
        verbose_name_plural = 'Контент сайта'

    def __str__(self):
        return f'{self.get_section_display()} — {self.title}'