from django.urls import path
from . import views

app_name = 'tables'

urlpatterns = [
    path('', views.TableListView.as_view(), name='home'),
    path('table/<int:pk>/', views.TableDetailView.as_view(), name='table_detail'),
]