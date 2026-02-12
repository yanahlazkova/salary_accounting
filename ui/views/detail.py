from django.views.generic import ListView, DetailView

from ui.buttons.registry import UIButtons
from ui.mixins.htmx import HTMXTemplateMixin


class UIDetailView(HTMXTemplateMixin, DetailView):
    """
    Базовий список для всіх HTMX-екранів
    """
    context_object_name = 'form_data'

    # Layout
    template_name = "base_page.html"
    htmx_template_name = "base_form_view.html"

    # UI metadata (перевизначаються у нащадках)
    page_blocks: list[str] | None = None
    form_content: list[str] | None = None
    page_subtitle: str | None = None
    form_title: str | None = None

    # набір кнопок
    toolbar_buttons: list[str] | None = None

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["page_blocks"] = self.page_blocks

        return ctx