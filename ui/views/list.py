from django.views.generic import ListView

from ui.mixins.htmx import HTMXTemplateMixin
from ui.mixins.page_toolbar import SectionPageToolbarMixin


class UIListView(HTMXTemplateMixin, ListView):
    """
    Базовий список для всіх HTMX-екранів
    """
    context_object_name = 'table_rows'

    # UI metadata (перевизначаються у нащадках)
    page_content: list[str] | None =  [
        'base_table.html'
    ]
    # paginate_by: int | None = None
    # page_subtitle: str | None = None
    table_titles: list[str] | None = None
    table_fields: list[str] | None = None
    toolbar_buttons: list[str] | None = None

    def get_page_content(self):
        return self.page_content

    def set_page_content(self, content_name):
        self.page_content.insert(0, content_name)

    def get_table_titles(self):
        """
        Повертає заголовки таблиці
        """
        if self.table_titles is not None:
            return self.table_titles

        if self.table_fields is not None:
            return [
                self.model._meta.get_field(f).verbose_name
                for f in self.table_fields
            ]

        return [
            f.verbose_name for f in self.model._meta.fields
        ]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["page_content"] = self.get_page_content()
        ctx["table_titles"] = self.get_table_titles()
        ctx['toolbar_buttons'] = self.get_toolbar_buttons()
        ctx['current_user'] = 'Гість' if str(self.request.user) == 'AnonymousUser' else self.request.user

        return ctx
