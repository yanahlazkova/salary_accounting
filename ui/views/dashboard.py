from dataclasses import dataclass, field

from django.db.models import Model
from django.db.models.sql import Query
from django.views.generic import TemplateView, DetailView

from ui.mixins.htmx import HTMXTemplateMixin
from ui.mixins.page_toolbar import SectionPageToolbarMixin
from ui.views.helper import get_obj_data, get_table_titles


@dataclass
class BlockOneObject(SectionPageToolbarMixin):
    app_label: str = None
    title: str = None
    data = None
    fields: dict = field(default_factory=dict)
    toolbar_buttons: list = field(default_factory=list)
    slug_field: str = None
    slug_url_kwargs: str = None

    def get_toolbar_buttons(self):
        if self.toolbar_buttons is None:
            return []
        return self.build_toolbar_buttons(self.toolbar_buttons, self.data)


@dataclass
class BlockTable(SectionPageToolbarMixin):
    app_label: str = None
    model = None
    name: str = None
    table_titles = None # : list = field(default_factory=list)
    table_rows: list = field(default_factory=list)
    toolbar_buttons: list = field(default_factory=list)
    slug_field: str = None
    slug_url_kwargs: str = None

    def get_toolbar_buttons(self):
        if self.toolbar_buttons is None:
            return []
        return self.build_toolbar_buttons(self.toolbar_buttons)

    def get_table_titles(self):
        return get_table_titles(self)


class UIDashboardView(HTMXTemplateMixin, TemplateView):
    """ UI для головної сторінки розділу меню, де відображаються окремо дані однієї моделі
    та окремо дані в вигляді таблиці іншої моделі """

    # блоки контенту:
    # перший у вигляді даних одного елемента з вказаної моделі
    # другий - таблиці даних вказаної моделі (може бути інша модель)
    page_content: tuple[str] = ('ui/base_form_dashboard.html', 'base_table.html',)

    # блок сторінки з одним елементом
    block_obj_model = None
    block_obj = None

    # Дані таблиці
    table_model = None
    block_table = None

    def get_page_content(self):
        # Перетворюємо на список тільки при виклику, щоб не псувати базовий атрибут
        return list(self.page_content)

    def build_toolbar_buttons(self,button_names=None, obj=None):
        return []  # Заглушка, щоб не було помилки

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx.update({
            "page_content": self.get_page_content(),
        })

        return ctx

