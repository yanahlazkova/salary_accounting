from django.views.generic import CreateView, DetailView

from settings.models import SocialSettings
from ui.mixins.htmx import HTMXTemplateMixin


class UICopyView(HTMXTemplateMixin, DetailView, CreateView):
    context_object_name = 'form_data'

    page_content: tuple[str] | None = ('base_form.html',)
    page_subtitle: str | None = None

    toolbar_buttons: list[str] | None = None

    def get_page_content(self):
        # Перетворюємо на список тільки при виклику, щоб не псувати базовий атрибут
        return list(self.page_content)

    def get_toolbar_buttons(self):
        return []  # Заглушка, щоб не було помилки

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx.update({
            "page_content": self.get_page_content(),
            'page_subtitle': self.page_subtitle,
            'toolbar_buttons': self.get_toolbar_buttons(),
        })

        for c in ctx:
            print(f'{c}: {ctx[c]}')

        return ctx