from django import forms

from .models import Booking


class BookingForm(forms.ModelForm):
    """
    Форма создания бронирования.

    ModelForm автоматически создаёт поля на основе модели:
    - Тип поля соответствует типу в БД (DateField → календарь, TimeField → выбор времени)
    - Валидация берётся из модели (clean, ограничения)
    """

    class Meta:
        model = Booking
        # Поля, которые заполняет клиент
        fields = ["table", "date", "time", "duration", "guests", "comment"]
        # Виджеты для красивого отображения
        widgets = {
            "date": forms.DateInput(
                attrs={
                    "type": "date",  # HTML5 календарь
                    "class": "form-control",
                    "min": "",  # Заполним через JavaScript сегодняшней датой
                }
            ),
            "time": forms.TimeInput(
                attrs={
                    "type": "time",  # HTML5 выбор времени
                    "class": "form-control",
                }
            ),
            "table": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "duration": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                    "max": "6",
                    "value": "2",
                }
            ),
            "guests": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                    "placeholder": "Количество гостей",
                }
            ),
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Особые пожелания (необязательно)",
                }
            ),
        }
        labels = {
            "table": "Столик",
            "date": "Дата",
            "time": "Время",
            "duration": "Длительность (часы)",
            "guests": "Количество гостей",
            "comment": "Комментарий",
        }

    def __init__(self, *args, **kwargs):
        """
        При создании формы фильтруем столики — показываем только активные.
        """
        super().__init__(*args, **kwargs)
        # Показываем только активные столики
        self.fields["table"].queryset = self.fields["table"].queryset.filter(
            is_active=True
        )
