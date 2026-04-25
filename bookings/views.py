from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone
from .models import Booking
from .forms import BookingForm


class BookingListView(LoginRequiredMixin, ListView):
    """
    Список бронирований текущего пользователя.

    ListView:
    - Автоматически получает список объектов из БД
    - По умолчанию ищет шаблон: <app>/<model>_list.html → bookings/booking_list.html
    - Передаёт в шаблон переменную object_list
    """
    model = Booking
    template_name = 'bookings/booking_list.html'
    context_object_name = 'bookings'  # В шаблоне будет переменная bookings

    def get_queryset(self):
        """
        Фильтруем бронирования — показываем только брони текущего пользователя.
        Сортировка: сначала будущие, потом прошедшие.
        """
        return Booking.objects.filter(
            user=self.request.user
        ).select_related('table')  # Оптимизация: подгружаем столики одним запросом


class BookingCreateView(LoginRequiredMixin, CreateView):
    """
    Создание нового бронирования.

    CreateView:
    - GET: показывает пустую форму
    - POST: проверяет данные, создаёт объект, перенаправляет
    """
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking_form.html'
    success_url = reverse_lazy('bookings:booking_list')

    def form_valid(self, form):
        """
        Вызывается, когда форма прошла валидацию.
        Привязываем бронь к текущему пользователю.
        """
        # Не сохраняем сразу (commit=False), чтобы добавить пользователя
        form.instance.user = self.request.user

        # Показываем сообщение об успехе
        messages.success(
            self.request,
            f'Столик успешно забронирован! Ожидайте подтверждения.'
        )

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Передаём в шаблон дополнительные данные.
        """
        context = super().get_context_data(**kwargs)
        # Передаём выбранный столик, если он передан в URL
        table_id = self.request.GET.get('table')
        if table_id:
            context['selected_table'] = table_id
        return context


class BookingDetailView(LoginRequiredMixin, DetailView):
    """
    Детальная информация о бронировании.

    DetailView:
    - Получает один объект по pk из URL
    - Шаблон: bookings/booking_detail.html
    """
    model = Booking
    template_name = 'bookings/booking_detail.html'
    context_object_name = 'booking'

    def get_queryset(self):
        """
        Пользователь может смотреть только свои бронирования.
        Администратор — все.
        """
        if self.request.user.is_admin_staff:
            return Booking.objects.all().select_related('user', 'table')
        return Booking.objects.filter(
            user=self.request.user
        ).select_related('table')


class BookingCancelView(LoginRequiredMixin, UpdateView):
    """
    Отмена бронирования.

    UpdateView используется для изменения статуса на 'cancelled'.
    """
    model = Booking
    fields = []  # Не показываем поля, только меняем статус
    template_name = 'bookings/booking_confirm_cancel.html'
    success_url = reverse_lazy('bookings:booking_list')

    def get_queryset(self):
        """
        Отменить можно только свои бронирования.
        """
        return Booking.objects.filter(user=self.request.user)

    def form_valid(self, form):
        """
        Меняем статус на 'cancelled' вместо удаления.
        """
        booking = self.get_object()

        # Проверяем, можно ли отменить (только pending или confirmed)
        if booking.status not in ['pending', 'confirmed']:
            messages.error(self.request, 'Это бронирование нельзя отменить.')
            return redirect('bookings:booking_list')

        booking.status = 'cancelled'
        booking.save()

        messages.success(self.request, 'Бронирование отменено.')
        return redirect(self.success_url)