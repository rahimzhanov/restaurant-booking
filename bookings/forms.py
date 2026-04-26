from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['table', 'date', 'time', 'duration', 'guests', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
            'time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
            }),
            'table': forms.Select(attrs={
                'class': 'form-select',
            }),
            'duration': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '6',
                'value': '2',
            }),
            'guests': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Количество гостей',
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Особые пожелания (необязательно)',
            }),
        }
        labels = {
            'table': 'Столик',
            'date': 'Дата',
            'time': 'Время',
            'duration': 'Длительность (часы)',
            'guests': 'Количество гостей',
            'comment': 'Комментарий',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['table'].queryset = self.fields['table'].queryset.filter(is_active=True)