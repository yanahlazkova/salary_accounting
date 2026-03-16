from dataclasses import dataclass, field

from django.views.generic import TemplateView

from ui.mixins.htmx import HTMXTemplateMixin


@dataclass
class BlockOneObject:
    title: str = None
    fields: dict = field(default_factory=dict)
    toolbar_buttons: list = field(default_factory=list)

    # def to_dict(self):
    #     return {
    #         'title': self.title,
    #         'fields': self.fields,
    #         'toolbar_buttons': self.toolbar_buttons,
    #     }
    #
    # def __str__(self):
    #     return str(self.to_dict())

@dataclass
class BlockTable:
    name: str = None
    table_titles: list = field(default_factory=list)
    table_rows: list = field(default_factory=list)
    toolbar_buttons: list = field(default_factory=list)

    # def to_dict(self):
    #     return {
    #         'name': self.table_name,
    #         'table_titles': self.table_titles,
    #         'table_rows': self.table_rows,
    #         'toolbar_buttons': self.toolbar_buttons,
    #     }
    #
    # def __str__(self):
    #     return str(self.to_dict())


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

