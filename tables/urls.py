from django.urls import path

from . import views

app_name = "tables"

urlpatterns = [
    path('', views.TableListView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('table/<int:pk>/', views.TableDetailView.as_view(), name='table_detail'),
    path('admin/tables/', views.TableAdminListView.as_view(), name='admin_table_list'),
    path('admin/tables/<int:pk>/', views.TableUpdateView.as_view(), name='admin_table_update'),
]
