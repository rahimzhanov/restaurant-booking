from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.contrib import messages


class AdminRequiredMixin(AccessMixin):
    """
    Миксин, который пускает только администраторов ресторана.

    AccessMixin — базовый класс для проверки доступа.
    Предоставляет метод handle_no_permission() для обработки отказа.
    """

    def dispatch(self, request, *args, **kwargs):
        """
        dispatch — точка входа для любого HTTP-запроса.

        Проверяем два условия:
        1. Пользователь авторизован (is_authenticated)
        2. У пользователя роль 'admin' (свойство is_admin_staff из модели)
        """
        if not request.user.is_authenticated:
            # Не вошёл — перенаправляем на страницу входа
            return self.handle_no_permission()

        if not request.user.is_admin_staff:
            # Вошёл, но не админ — показываем ошибку и перенаправляем
            messages.error(request, 'Доступ запрещён. Требуются права администратора.')
            return redirect('tables:home')

        # Всё хорошо — выполняем запрос как обычно
        return super().dispatch(request, *args, **kwargs)