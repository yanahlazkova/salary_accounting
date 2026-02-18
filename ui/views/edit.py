from django.contrib.auth.models import User
from django.views.generic import UpdateView

from ui.forms.base import BaseHTMXForm
from ui.mixins.htmx import HTMXTemplateMixin


class UIEditView(HTMXTemplateMixin, UpdateView):
    """ Базовий клас для редагування об'єктів """
    context_object_name = 'form_data'
    page_content: tuple[str] | None = ('base_form.html',)
    page_subtitle: dict | None = None

    # набір кнопок
    toolbar_buttons: list[str] | None = None

    def get_page_content(self):
        # Перетворюємо на список тільки при виклику, щоб не псувати базовий атрибут
        return list(self.page_content)

    def get_toolbar_buttons(self):
        return [] # заглушка

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx.update({
            "page_content": self.get_page_content(),
            'page_subtitle': self.page_subtitle,
            'toolbar_buttons': self.get_toolbar_buttons(),
            'form': self.get_object(),
        })
        return ctx