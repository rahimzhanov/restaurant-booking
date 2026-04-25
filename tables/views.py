from django.core.checks import messages
from django.urls import reverse_lazy
from django.views.generic import (DetailView, ListView, UpdateView)
from bookings.mixins import AdminRequiredMixin

from .models import Table


class TableListView(ListView):
    """
    Главная страница со списком всех столиков.
    """

    model = Table
    template_name = "tables/table_list.html"
    context_object_name = "tables"

    def get_queryset(self):
        """
        Показываем только активные столики.
        """
        return Table.objects.filter(is_active=True).order_by("number")


class TableDetailView(DetailView):
    """
    Детальная информация о столике + форма бронирования.
    """

    model = Table
    template_name = "tables/table_detail.html"
    context_object_name = "table"

    def get_context_data(self, **kwargs):
        """
        Передаём в шаблон форму бронирования.
        """
        context = super().get_context_data(**kwargs)
        from bookings.forms import BookingForm

        context["booking_form"] = BookingForm(initial={"table": self.object})
        return context


class TableAdminListView(AdminRequiredMixin, ListView):
    """
    Список столиков для управления администратором.
    Показываем все столики, включая неактивные.
    """

    model = Table
    template_name = "tables/admin_table_list.html"
    context_object_name = "tables"

    def get_queryset(self):
        return Table.objects.all().order_by("number")


class TableUpdateView(AdminRequiredMixin, UpdateView):
    """
    Редактирование столика администратором.
    """

    model = Table
    fields = ["number", "seats", "location", "is_active", "description"]
    template_name = "tables/admin_table_form.html"
    success_url = reverse_lazy("tables:admin_table_list")

    def form_valid(self, form):
        messages.success(self.request, f"Столик №{self.object.number} обновлён.")
        return super().form_valid(form)
