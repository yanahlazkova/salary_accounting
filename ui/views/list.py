from django.views.generic import ListView

from ui.mixins.htmx import HTMXTemplateMixin
from ui.mixins.page_toolbar import SectionPageToolbarMixin


class UIListView(HTMXTemplateMixin, ListView):
    """
    Базовий список для всіх HTMX-екранів
    """
    context_object_name = 'table_rows'

    # UI metadata (перевизначаються у нащадках)
    table_name: str | None = None
    # Використовуємо кортеж (tuple), він незмінний — це безпечніше
    page_content: tuple[str] = ('base_table.html',)
    table_titles: list[str] | None = None
    table_fields: list[str] | None = None
    toolbar_buttons: list[str] | None = None

    def get_page_content(self):
        # Перетворюємо на список тільки при виклику, щоб не псувати базовий атрибут
        return list(self.page_content)

    def get_toolbar_buttons(self):
        return []  # Заглушка, щоб не було помилки

    # def set_page_content(self, content_name):
    #     # content = self.get_page_content()
    #     self.page_content = tuple(self.get_page_content().insert(0, content_name))
    #     print(f'UIListView: {self.page_content}')

    def get_table_titles(self):
        """
        Повертає заголовки таблиці
        """
        if self.table_titles is not None:
            return self.table_titles

        fields_to_check = self.table_fields or [f.name for f in self.model._meta.fields]
        return [
            self.model._meta.get_field(f).verbose_name
            for f in fields_to_check
        ]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx.update({
            "page_content": self.get_page_content(),
            "table_titles": self.get_table_titles(),
            "toolbar_buttons": self.get_toolbar_buttons(),
            "table_names": self.table_name,
        })

        return ctx
