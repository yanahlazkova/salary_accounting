from django.views.generic import ListView
from ui.mixins.htmx import HTMXTemplateMixin


class UIListView(HTMXTemplateMixin, ListView):
    """
    Базовий список для всіх HTMX-екранів
    """
    context_object_name = 'table_rows'

    table_action = [] # набір кнопок

    # Layout
    template_name = "base_page.html"
    htmx_template_name = "base_content.html"

    # UI metadata (перевизначаються у нащадках)
    page_title: str | None = None
    page_icon: str | None = None
    page_blocks: list[str] | None = None
    paginate_by: int | None = None
    table_titles: list[str] | None = None
    table_fields: list[str] | None = None

    def get_page_title(self):
        return self.page_title

    def get_page_icon(self):
        return self.page_icon

    def get_page_blocks(self):
        return self.page_blocks

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

    def get_table_action(self):
        return self.table_action

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["page_title"] = self.get_page_title()
        ctx["page_icon"] = self.get_page_icon()
        ctx["page_blocks"] = self.get_page_blocks()
        ctx["table_titles"] = self.get_table_titles()
        ctx["table_action"] = self.get_table_action()

        return ctx
