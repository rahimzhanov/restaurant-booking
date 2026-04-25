from django.urls import path

from . import views

app_name = "bookings"

urlpatterns = [
    path("", views.BookingListView.as_view(), name="booking_list"),
    path("create/", views.BookingCreateView.as_view(), name="booking_create"),
    path("<int:pk>/", views.BookingDetailView.as_view(), name="booking_detail"),
    path("<int:pk>/cancel/", views.BookingCancelView.as_view(), name="booking_cancel"),
    # Профиль теперь будет в bookings
    path("profile/", views.BookingListView.as_view(), name="profile"),
    # Административные URL
    path(
        "admin/bookings/",
        views.AdminBookingListView.as_view(),
        name="admin_booking_list",
    ),
    path(
        "admin/bookings/<int:pk>/",
        views.AdminBookingUpdateView.as_view(),
        name="admin_booking_update",
    ),
]
