from django.urls import path

from . import views

app_name = "tables"

urlpatterns = [
    path("", views.TableListView.as_view(), name="home"),
    path("table/<int:pk>/", views.TableDetailView.as_view(), name="table_detail"),
    # Административные URL
    path("admin/tables/", views.TableAdminListView.as_view(), name="admin_table_list"),
    path(
        "admin/tables/<int:pk>/",
        views.TableUpdateView.as_view(),
        name="admin_table_update",
    ),
]
