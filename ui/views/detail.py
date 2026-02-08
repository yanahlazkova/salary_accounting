from django.views.generic import ListView, DetailView

from ui.buttons.registry import UIButtons
from ui.mixins.htmx import HTMXTemplateMixin


class UIDetailView(HTMXTemplateMixin, DetailView):
    """
    Базовий список для всіх HTMX-екранів
    """
    context_object_name = 'form_data'

    table_action = [] # набір кнопок

    # Layout
    template_name = "base_page_form.html"
    htmx_template_name = "base_form_view.html"

    # UI metadata (перевизначаються у нащадках)
    form_content: list[str] | None = None
    form_title: str | None = None

    def get_form_content(self):
        return self.form_content

    def get_table_action(self):
        return self.table_action

    def get_form_title(self):
        return self.form_title

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["form_content"] = self.get_form_content()
        ctx["table_action"] = self.get_table_action()
        ctx["form_title"] = self.get_form_title()

        return ctx