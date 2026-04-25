from django.views.generic import ListView, DetailView
from .models import Table


class TableListView(ListView):
    """
    Главная страница со списком всех столиков.
    """
    model = Table
    template_name = 'tables/table_list.html'
    context_object_name = 'tables'

    def get_queryset(self):
        """
        Показываем только активные столики.
        """
        return Table.objects.filter(is_active=True).order_by('number')


class TableDetailView(DetailView):
    """
    Детальная информация о столике + форма бронирования.
    """
    model = Table
    template_name = 'tables/table_detail.html'
    context_object_name = 'table'

    def get_context_data(self, **kwargs):
        """
        Передаём в шаблон форму бронирования.
        """
        context = super().get_context_data(**kwargs)
        from bookings.forms import BookingForm
        context['booking_form'] = BookingForm(initial={'table': self.object})
        return context