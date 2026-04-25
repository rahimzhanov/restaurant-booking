from django.urls import path
from django.views.generic import TemplateView

app_name = 'bookings'

urlpatterns = [
    # Временные заглушки, заменим на реальные views на Этапе 3
    path('', TemplateView.as_view(template_name='bookings/booking_list.html'), name='booking_list'),
    path('profile/', TemplateView.as_view(template_name='users/profile.html'), name='profile'),
    path('admin/', TemplateView.as_view(template_name='bookings/admin_booking_list.html'), name='admin_booking_list'),
]