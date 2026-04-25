from django.urls import path
from django.views.generic import TemplateView

app_name = 'tables'

urlpatterns = [
    # Временная заглушка для главной страницы
    path('', TemplateView.as_view(template_name='tables/home.html'), name='home'),
]