from django.views.generic import ListView
from ui.mixins.htmx import HTMXTemplateMixin


class UIListView(HTMXTemplateMixin, ListView):
    """
    Базовий список для всіх HTMX-екранів
    """

    # Layout
    template_name = "base_page.html"
    htmx_template_name = "base_content.html"

    # UI metadata (перевизначаються у нащадках)
    page_title: str | None = None
    page_icon: str | None = None
    page_blocks: list[str] | None = None
    paginate_by: int | None = None

    def get_page_title(self):
        return self.page_title

    def get_page_icon(self):
        return self.page_icon

    def get_page_blocks(self):
        return self.page_blocks

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["page_title"] = self.get_page_title()
        ctx["page_icon"] = self.get_page_icon()
        ctx["page_blocks"] = self.get_page_blocks()

        return ctx
