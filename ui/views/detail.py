from django.views.generic import ListView, DetailView

from ui.buttons.registry import UIButtons
from ui.mixins.htmx import HTMXTemplateMixin
from ui.views.helper import get_obj_fields


class UIDetailView(HTMXTemplateMixin, DetailView):
    """
    Базовий список для всіх HTMX-екранів
    Виводить детальну інформацію обраного об'єкта
    """
    context_object_name = 'form_data'

    # UI metadata (перевизначаються у нащадках)
    page_content: tuple[str] | None = ('base_form_view.html',)
    page_subtitle: dict | None = None

    # набір кнопок
    toolbar_buttons: list[str] | None = None

    def get_page_content(self):
        # Перетворюємо на список тільки при виклику, щоб не псувати базовий атрибут
        return list(self.page_content)

    def get_toolbar_buttons(self):
        return []  # Заглушка, щоб не було помилки

    # def get_form_data(self):
    #     obj = self.get_object()
    #
    #     return {
    #         field.verbose_name: getattr(obj, field.name)
    #         for field in obj._meta.fields
    #     }



    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        field, info = get_obj_fields(self.object)

        ctx.update({
            "page_content": self.get_page_content(),
            'page_subtitle': self.page_subtitle,
            'toolbar_buttons': self.get_toolbar_buttons(),
            # 'fields': model_to_fields(self.object),
            'fields': field,
            'info': info,
        })

        return ctx
