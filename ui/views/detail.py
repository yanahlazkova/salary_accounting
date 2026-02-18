from django.views.generic import ListView, DetailView

from ui.buttons.registry import UIButtons
from ui.mixins.htmx import HTMXTemplateMixin


class UIDetailView(HTMXTemplateMixin, DetailView):
    """
    Базовий список для всіх HTMX-екранів
    """
    context_object_name = 'form_data'

    # UI metadata (перевизначаються у нащадках)
    page_content: list[str] | None = ['base_form_view.html']
    # form_content: list[str] | None = None
    page_subtitle: dict | None = None
    # form_title: str | None = None

    # набір кнопок
    toolbar_buttons: list[str] | None = None

    def get_page_subtitle(self, page_name) -> str:
        return self.page_subtitle if self.page_subtitle[page_name] else ''


    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # obj = super().get_object()
        # print(f'obj: {obj}')

        ctx["page_content"] = self.page_content
        # ctx['page_subtitle'] = self.get_page_subtitle('view')
        ctx['toolbar_buttons'] = self.get_toolbar_buttons()
        ctx['current_user'] = 'Гість' if str(self.request.user) == 'AnonymousUser' else self.request.user


        return ctx